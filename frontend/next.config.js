/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'via.placeholder.com',
        port: '',
        pathname: '/**',
      },
    ],
    // Allow unoptimized images for placeholder service
    unoptimized: false,
    // Disable image optimization for external images if needed
    loader: 'default',
  },
}

module.exports = nextConfig

