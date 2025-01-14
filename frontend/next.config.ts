import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Reactの厳密モードを有効化
  reactStrictMode: true,

  // プロキシ設定
  async rewrites() {
    return [
      {
        source: "/api/:path*", // フロントエンドのAPIパス
        destination: "http://localhost:8000/api/:path*", // バックエンドのエンドポイント
      },
    ];
  },
};

export default nextConfig;
