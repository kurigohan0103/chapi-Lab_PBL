"use client";

import { useState } from "react";
import { useRouter } from 'next/navigation';
import axios from 'axios';


export default function Login() {

    // ユーザーが入力したユーザー名とパスワードを保存するための状態変数
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const router = useRouter();

    // "ログイン"処理を行う非同期関数
    const handleLogin = async () => {
        try {
            const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
                username,
                password,
            });
            console.log('Login successful:', response.data)
            localStorage.setItem('token', response.data.access_token)
            router.push('/home')

            // 受け取ったアクセストークンをブラウザのローカルストレージに保存
            localStorage.setItem('token', response.data.access_token);
        } catch (error: unknown) {
            // エラーがオブジェクトかどうかを確認
            if (error instanceof Error) {
                console.error('Login failed:', error.message);
            } else {
                console.error('An unknown error occurred');
            }      
        }
    };

    return (
        <div>
            <h1>Login</h1>
            <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            <button onClick={handleLogin}>Login</button>
        </div>
    )
}