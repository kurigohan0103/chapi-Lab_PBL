"use client";

// import { useState } from "react";
// import axios from 'axios';


export default function Logout() {
    // ログアウト処理を行う関数
    const handleLogout = () => {
      // ローカルストレージからトークンを削除
      localStorage.removeItem('token');
      alert('Logged out successfully'); // ログアウト成功時のアラート
      console.log('User logged out'); // ログアウトログをコンソールに出力
    };
  
    return (
      <div>
        <h1>Logout</h1>
        <button onClick={handleLogout}>Logout</button> {/* ログアウトボタン */}
      </div>
    );
}