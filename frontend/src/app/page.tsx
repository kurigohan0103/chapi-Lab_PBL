"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import "../styles/Home.css";
import "../styles/moretoggles.min.css";

export default function Home() {
    const [securityMode, setSecurityMode] = useState<boolean>(false); // セキュリティモード
    const [isLoading, setIsLoading] = useState<boolean>(true); // ローディング状態

    // セキュリティモードを取得する関数
    const fetchSecurityMode = async () => {
        setIsLoading(true);
        try {
            const response = await fetch("/api/security_mode"); // バックエンドAPIを呼び出し
            if (response.ok) {
                const data = await response.json();
                setSecurityMode(data.mode); // 取得したモードをセット
            } else {
                console.error("Failed to fetch security mode");
            }
        } catch (error) {
            console.error("Error fetching security mode:", error);
        } finally {
            setIsLoading(false);
        }
    };

    // セキュリティモードを更新する関数
    const updateSecurityMode = async (newMode: boolean) => {
        try {
            const response = await fetch("/api/security_mode", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ mode: newMode }),
            });
            if (response.ok) {
                const data = await response.json();
                setSecurityMode(data.mode); // 更新後のモードをセット
            } else {
                console.error("Failed to update security mode");
            }
        } catch (error) {
            console.error("Error updating security mode:", error);
        }
    };

    // ページロード時にセキュリティモードを取得
    useEffect(() => {
        fetchSecurityMode();
    }, []);

    // トグルスイッチの変更時にセキュリティモードを更新
    const handleToggleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const newMode = event.target.checked;
        updateSecurityMode(newMode);
    };

    return (
        <div className="home-container">

            {isLoading ? (
                <p>Loading...</p>
            ) : (
                <>
                    {/* セキュリティモードの状態に応じた画像を表示 */}
                    <Image
                        src={securityMode ? "/images/security-on.png" : "/images/security-off.png"}
                        alt="Security Mode Icon"
                        width={200}
                        height={200}
                        className="robot-image"
                    />
                    <h2 className="security-mode-text">
                        Security Mode: {securityMode ? "ON" : "OFF"}
                    </h2>

                    {/* トグルスイッチ */}
                    <div className="mt-transparent" style={{ fontSize: "10px" }}>
                        <input
                            id="toggle-1"
                            type="checkbox"
                            checked={securityMode}
                            onChange={handleToggleChange}
                        />
                        <label htmlFor="toggle-1"></label>
                    </div>
                </>
            )}
        </div>
    );
}
