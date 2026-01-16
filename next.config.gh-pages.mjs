/** @type {import('next').NextConfig} */
// Configuration for GitHub Pages (static export only - limited functionality)
// Note: Dynamic routes and API calls won't work in static export
const nextConfig = {
  output: 'export',
  basePath: '/BoxMachiBox-',
  assetPrefix: '/BoxMachiBox-/',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
};

export default nextConfig;
