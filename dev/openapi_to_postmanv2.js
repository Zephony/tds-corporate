const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// --- CLI Flags ---
const args = process.argv.slice(2);
const getFlagValue = (flag) => {
  const index = args.indexOf(flag);
  return index !== -1 && args[index + 1] ? args[index + 1] : null;
};

const inputFile = getFlagValue('--input'); // local file path
const inputUrl = getFlagValue('--url');    // remote URL to OpenAPI JSON
const outputFile = getFlagValue('--output');
const postmanApiKey = getFlagValue('--apikey');
const workspaceId = getFlagValue('--workspace');

if ((!inputFile && !inputUrl) || !outputFile || !postmanApiKey) {
  console.error('Usage: node convert_group_by_tags.js --input openapi.json OR --url http://... --output collection.json --apikey <POSTMAN_API_KEY> [--workspace <WORKSPACE_ID>]');
  process.exit(1);
}

// --- Step 0: Get OpenAPI JSON ---
async function loadOpenApi() {
  if (inputUrl) {
    console.log(`🌐 Downloading OpenAPI spec from ${inputUrl} ...`);
    const res = await fetch(inputUrl);
    if (!res.ok) throw new Error(`Failed to download OpenAPI JSON: ${res.status} ${res.statusText}`);
    return await res.json();
  } else {
    if (!fs.existsSync(inputFile)) throw new Error(`Input file not found: ${inputFile}`);
    return JSON.parse(fs.readFileSync(inputFile, 'utf8'));
  }
}

(async () => {
  try {
    console.log('🔄 Converting OpenAPI to Postman collection...');
    const openapi = await loadOpenApi();

    let filterableFieldsMap = {};
    try {
      const filterableStdout = execSync('python dev/get_filterable_fields.py', { encoding: 'utf8' });
      filterableFieldsMap = JSON.parse(filterableStdout);
    } catch (err) {
      console.warn('⚠️  Unable to load filterable fields map, continuing without query param augmentation.');
    }

    // Save temp openapi file for npx converter
    const tempOpenApiFile = path.join(__dirname, 'temp_openapi.json');
    fs.writeFileSync(tempOpenApiFile, JSON.stringify(openapi, null, 2));

    // Step 1: Convert OpenAPI → Postman via npx
    const tempFile = path.join(__dirname, 'temp_postman_collection.json');
    // console.log('📦 Converting OpenAPI to Postman collection...');
    execSync(`npx openapi-to-postmanv2 -s "${tempOpenApiFile}" -o "${tempFile}" -p`, { stdio: null });
    
    // Post-process the collection to fix indentation in request bodies
    const tempCollection = JSON.parse(fs.readFileSync(tempFile, 'utf8'));
    
    function fixRequestBodyIndentation(items) {
      for (const item of items) {
        if (item.item) {
          fixRequestBodyIndentation(item.item);
        } else if (item.request?.body?.raw) {
          try {
            const body = JSON.parse(item.request.body.raw);
            item.request.body.raw = JSON.stringify(body, null, 4);
          } catch (e) {
            // Not JSON, leave as is
          }
        }
      }
    }
    
    function convertUrlParameters(items) {
      for (const item of items) {
        if (item.item) {
          convertUrlParameters(item.item);
        } else if (item.request?.url?.path) {
          // Convert path parameters from :param to {{param}} format
          item.request.url.path = item.request.url.path.map(segment => {
            if (typeof segment === 'string' && segment.startsWith(':')) {
              return `{{${segment.substring(1)}}}`;
            }
            return segment;
          });
        }
      }
    }

    function setDefaultPaginationQueryParams(items) {
      for (const item of items) {
        if (item.item) {
          setDefaultPaginationQueryParams(item.item);
          continue;
        }

        const queryParams = item.request?.url?.query;
        if (!Array.isArray(queryParams)) {
          continue;
        }

        queryParams.forEach(param => {
          if (!param?.key) {
            return;
          }

          const key = param.key.toLowerCase();
          if (key === 'page' || key === 'page_size') {
            param.value = '1';
          }
        });
      }
    }

    fixRequestBodyIndentation(tempCollection.item);
    convertUrlParameters(tempCollection.item);
    setDefaultPaginationQueryParams(tempCollection.item);
    fs.writeFileSync(tempFile, JSON.stringify(tempCollection, null, 2));

    // Step 2: Group by tags only, flatten all requests into tag folders
    console.log('📂 Grouping requests by tags...');
    const collection = JSON.parse(fs.readFileSync(tempFile, 'utf8'));

    function extractAllRequests(items) {
      let requests = [];
      for (const item of items) {
        if (item.item) {
          requests = requests.concat(extractAllRequests(item.item));
        } else {
          requests.push(item);
        }
      }
      return requests;
    }

    // Build tags mapping from OpenAPI spec
    const requestTags = {};
    console.log('🔍 OpenAPI paths found:');
    for (const [pathKey, methods] of Object.entries(openapi.paths)) {
      for (const [method, op] of Object.entries(methods)) {
        if (op && op.tags && Array.isArray(op.tags)) {
          const methodUpper = method.toUpperCase();
          const key = `${methodUpper} ${pathKey}`;
          requestTags[key] = op.tags;
          console.log(`   ${key} -> ${op.tags.join(', ')}`);
        }
      }
    }

    const allRequests = extractAllRequests(collection.item);
    const tagFolders = {};

    for (const req of allRequests) {
      const method = req.request?.method || '';
      const path = req.request?.url?.path?.join('/') || '';
      const pathStr = `/${path}`;
      
      // Normalize path to match OpenAPI format
      const normalizedPath = pathStr
        .replace(/\/$/, '') // Remove trailing slash
        .replace(/\/+/g, '/') // Replace multiple slashes with single
        .replace(/^\/+/, '/'); // Ensure single leading slash
      
      // Convert Postman parameter format (:param) to OpenAPI format ({param})
      const openApiPath = normalizedPath.replace(/\/:([^\/]+)/g, '/{$1}');
      
      // Also convert Postman variable format ({{param}}) to OpenAPI format ({param})
      const openApiPathFromVariable = normalizedPath.replace(/\/\{\{([^}]+)\}\}/g, '/{$1}');
      
      // Try multiple path formats to match
      const possibleKeys = [
        `${method.toUpperCase()} ${openApiPath}`,
        `${method.toUpperCase()} ${openApiPathFromVariable}`,
        `${method.toUpperCase()} ${normalizedPath}`,
        `${method.toUpperCase()} ${normalizedPath.substring(1)}`, // Without leading slash
        `${method.toUpperCase()} ${pathStr}`,
        `${method.toUpperCase()} ${path}`,
        `${method.toUpperCase()} ${pathStr.replace(/\/$/, '')}`,
        `${method.toUpperCase()} ${path.replace(/\/$/, '')}`
      ];
      
      let tags = ['Ungrouped'];
      for (const key of possibleKeys) {
        if (requestTags[key]) {
          tags = requestTags[key];
          console.log(`✅ Matched: ${req.name} -> ${key} -> ${tags.join(', ')}`);
          break;
        }
      }
      if (tags[0] === 'Ungrouped') {
        console.log(`❌ No match for: ${req.name} (${method} ${normalizedPath})`);
        console.log(`   Available keys: ${Object.keys(requestTags).slice(0, 5).join(', ')}...`);
      }
      
      for (const tag of tags) {
        if (!tagFolders[tag]) tagFolders[tag] = [];
        tagFolders[tag].push(req);
      }
    }

    collection.item = Object.entries(tagFolders).map(([tagName, requests]) => ({
      name: tagName,
      item: requests
    }));

    function applyFilterableQueryParams(items) {
      for (const item of items) {
        if (item.item) {
          applyFilterableQueryParams(item.item);
          continue;
        }

        const request = item.request;
        if (!request || (request.method || '').toUpperCase() !== 'GET') {
          continue;
        }

        const url = request.url;
        if (!url || !Array.isArray(url.path)) {
          continue;
        }

        const adminIndex = url.path.findIndex(segment => segment === 'admin');
        if (adminIndex === -1 || adminIndex + 1 >= url.path.length) {
          continue;
        }

        const resourceSegment = url.path[adminIndex + 1];
        if (!resourceSegment || resourceSegment.includes('{{') || resourceSegment.includes(':')) {
          continue;
        }

        const tableName = resourceSegment.replace(/-/g, '_');
        const fields = filterableFieldsMap[tableName];
        if (!Array.isArray(fields) || !fields.length) {
          continue;
        }

        if (!Array.isArray(url.query)) {
          url.query = [];
        }

        const existingKeys = new Set(url.query.map(param => param.key));

        fields.forEach(fieldName => {
          const paramKey = `f_${fieldName}`;
          if (existingKeys.has(paramKey)) {
            return;
          }
          url.query.push({
            key: paramKey,
            value: '',
            description: `Filter by ${fieldName}`,
          });
        });
      }
    }

    applyFilterableQueryParams(collection.item);

    fs.writeFileSync(outputFile, JSON.stringify(collection, null, 4));
    fs.unlinkSync(tempFile);
    fs.unlinkSync(tempOpenApiFile);
    // console.log(`✅ Grouped collection saved to ${path.resolve(outputFile)}`);

    // Step 3: Push to Postman using fetch
    const headers = {
      'X-Api-Key': postmanApiKey,
      'Content-Type': 'application/json'
    };

    let existingCollection = null;
    if (workspaceId) {
      const res = await fetch(`https://api.getpostman.com/collections?workspace=${workspaceId}`, { headers });
      const data = await res.json();
      existingCollection = data.collections.find(c => c.name === collection.info.name);
    } else {
      const res = await fetch('https://api.getpostman.com/collections', { headers });
      const data = await res.json();
      existingCollection = data.collections.find(c => c.name === collection.info.name);
    }

    if (existingCollection) {
      console.log(`🔄 Updating existing collection: ${existingCollection.name}`);
      const res = await fetch(`https://api.getpostman.com/collections/${existingCollection.uid}`, {
        method: 'PUT',
        headers,
        body: JSON.stringify({ collection })
      });
      if (!res.ok) throw new Error(await res.text());
      // console.log('✅ Collection updated successfully.');
    } else {
      console.log(`➕ Creating new collection: ${collection.info.name}`);
      const url = workspaceId
        ? `https://api.getpostman.com/collections?workspace=${workspaceId}`
        : `https://api.getpostman.com/collections`;
      const res = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify({ collection })
      });
      if (!res.ok) throw new Error(await res.text());
      // console.log('✅ Collection created successfully.');
    }

  } catch (err) {
    console.error('❌ Error:', err.message);
  } finally {
    // Clean up temp files
    if (fs.existsSync(outputFile)) fs.unlinkSync(outputFile);
  }
})();
