/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: '/BoxMachiBox-',
  assetPrefix: '/BoxMachiBox-/',
  images: {
    unoptimized: true,
  },
  trailingSlash: true,
  eslint: {
    ignoreDuringBuilds: true, // Add this line
  },
  typescript: {
    ignoreBuildErrors: true, // Add this line too
  },
};

export default nextConfig;
