"use client";
import { useRouter } from 'next/navigation';


export default function Logout() {

    const router = useRouter();

    // ログアウト処理を行う関数
    const handleLogout = () => {
      // ローカルストレージからトークンを削除
      localStorage.removeItem('token');
      // ログアウト成功時のアラート
      alert('Logged out successfully');
      // ログアウトログをコンソールに出力
      console.log('User logged out');
      router.push('/');
    };
  
    return (
      <div>
        <h1>Logout</h1>
        <button onClick={handleLogout}>Logout</button> {/* ログアウトボタン */}
      </div>
    );
}