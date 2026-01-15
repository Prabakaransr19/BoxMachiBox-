/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export', // Enable static HTML export
  basePath: '/BoxMachiBox-', // Your repository name
  assetPrefix: '/BoxMachiBox-/', // Ensure assets load correctly
  images: {
    unoptimized: true, // Required for static export
  },
  trailingSlash: true, // Adds trailing slashes to URLs
};

export default nextConfig;
