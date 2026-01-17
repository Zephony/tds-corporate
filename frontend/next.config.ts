import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Removed standalone mode to fix static file serving
  // output: 'standalone',
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  // Ensure Next writes a BUILD_ID so `next start` works reliably across versions
  generateBuildId: async () => {
    return process.env.NEXT_BUILD_ID || Date.now().toString(36);
  },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://backend:9999/api/:path*',
      },
      {
        source: '/uploads/:path*',
        destination: 'http://backend:9999/uploads/:path*',
      },
      {
        source: '/files/:path*',
        destination: 'http://backend:9999/files/:path*',
      },
    ];
  },
};

export default nextConfig;
