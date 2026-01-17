import { NextRequest, NextResponse } from 'next/server';

export const config = {
  matcher: ['/api/:path*'],
};

export function middleware(request: NextRequest) {
  const jwt = request.cookies.get('jwt')?.value;

  if (!jwt) {
    return NextResponse.next();
  }

  const requestHeaders = new Headers(request.headers);
    console.log("Middleware JWT:", jwt);

  if (!requestHeaders.has('authorization')) {
    requestHeaders.set('authorization', `Bearer ${jwt}`);
      console.log("Authorization header added");
  }

  return NextResponse.next({ request: { headers: requestHeaders } });
}
