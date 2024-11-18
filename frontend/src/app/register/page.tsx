// このファイル全体をクライアントコンポーネントとして扱う．
// これにより，クライアント専用のReactフックを使用できるようになる．
"use client";

import {useState} from "react";
import { useRouter } from 'next/navigation';
import axios from 'axios';


export default function Register() {

    // const [state, setState] = useState(false);
    // state: 現在の値, setState: stateの状態を変更する関数, false: 初期値
    const  [username, setUsername] = useState("");
    const  [password, setPassword] = useState("");

    const router = useRouter();

    // "登録"処理を行う非同期関数
    const handleRegister = async () => {

        try {
            // API エンドポイントに対してPOSTリクエストを送信
            const response = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/auth/register`, {
                username,
                password,
            });
            console.log('Registration successful:', response.data);
            alert('Registration successful'); // 登録成功時のアラート
            router.push('/login');

        // tryブロックで発生したエラーがerror変数に格納され，catchブロックの中でそのエラーを処理できるようにしている
        } catch (error: unknown) {
            if (axios.isAxiosError(error)) {
                console.error('Registration failed:', error.response?.data || error.message);
                alert(`Error: ${JSON.stringify(error.response?.data) || error.message}`);
            } else {
                console.error('An unknown error occurred');
                alert('An unknown error occurred');
            }
        }
    };

    return (
        <div>
            <h1>Register</h1>
            <input
                // テキスト入力ができることを指定
                type="text"
                // 入力フィールドが空のときの表示
                placeholder="Username"
                // 状態変数usernameの値をフィールドに表示
                value={username}
                // 入力内容が変更されたときに呼び出され，passwordの状態を更新
                onChange={(e) => setUsername(e.target.value)}
            />
            <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            
            {/*ボタンがクリックされるとhandleRegister関数が呼び出される */}
            <button onClick={handleRegister}>Register</button>
        </div>
    )
}