import axios from 'axios';


// apiという名前のaxiosインスタンスを作成
const api = axios.create({
    // 環境変数に基づいてベースURLを設定
    // NEXT_PUBLIC接頭辞により環境変数がフロントエンド（ブラウザ側）でアクセス可能
    baseURL: process.env.NEXT_PUBLIC_API_URL, 
});

// トークンをリクエストのヘッダーに自動的に追加するインターセプターを設定
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// 作成した api インスタンスをデフォルトエクスポート
// これで他のファイルで api をインポートして使用することができる
export default api;