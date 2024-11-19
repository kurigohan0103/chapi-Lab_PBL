"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect } from "react";
import "../../styles/Home.css";
import "../../node_modules/moretoggles/output/moretoggles.min.css";

export default function Home() {
    // トグルの変更イベントを設定
    useEffect(() => {
        const toggle = document.getElementById("toggle-1") as HTMLInputElement;
        toggle.addEventListener("change", (event) => {
            const target = event.target as HTMLInputElement;
            if (toggle.checked) {
                alert("トグルがオンになりました");
                // 後で消す
                alert(target)
            } else {
                alert("トグルがオフになりました");
            }
            
        });

        // クリーンアップ関数
        return () => toggle.removeEventListener("change", () => {});
    }, []);

    return (
        <div className="home-container">
            <h1>HOME</h1>
            <Image
                src="/image/security-mode-icon.png"
                alt="Robot Illustration"
                width={200}
                height={200}
                className="robot-image"
            />
            <h2 className="security-mode-text">Security Mode</h2>

            {/* トグルスイッチ*/}
            <div className="mt-transparent" style={{ fontSize: "10px" }}>
                <input id="toggle-1" type="checkbox" />
                <label htmlFor="toggle-1"></label>
            </div>

            <Link href="/robot">
                <button className="action-button">Detail</button>
            </Link>
        </div>
    );
}
