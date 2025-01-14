import Link from "next/link";
import { useState, useEffect } from "react";
import Image from "next/image";
import "../styles/Header.css";

export default function Header() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [touchStartX, setTouchStartX] = useState(0);

    // メニューの表示・非表示を切り替える関数
    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    // メニューを閉じる関数
    const closeMenu = () => {
        setIsMenuOpen(false);
    };

    // スワイプ検出のための関数
    const handleTouchStart = (e: TouchEvent) => {
        setTouchStartX(e.touches[0].clientX);
    };

    const handleTouchEnd = (e: TouchEvent) => {
        const touchEndX = e.changedTouches[0].clientX;
        if (touchStartX - touchEndX > 50) {
            closeMenu(); // 左にスワイプしたらメニューを閉じる
        }
    };

    // スワイプイベントリスナーを追加
    useEffect(() => {
        window.addEventListener("touchstart", handleTouchStart);
        window.addEventListener("touchend", handleTouchEnd);

        return () => {
            window.removeEventListener("touchstart", handleTouchStart);
            window.removeEventListener("touchend", handleTouchEnd);
        };
    }, [touchStartX]);

    return (
        <header className="header">
            {/* 左端のアイコンボタン */}
            <button className="menu-icon" onClick={toggleMenu}>
            <Image
                    src="/images/menu-icon.png"
                    alt="Menu Icon"
                    width={50}
                    height={50}
                />
            </button>

            {/* ナビゲーションメニュー */}
            <nav className={`nav-menu ${isMenuOpen ? "open" : ""}`}>
                <ul>
                    <li>
                        <Link href="/" onClick={closeMenu}>HOME</Link>
                    </li>
                    <li>
                        <Link href="/robot" onClick={closeMenu}>Robot</Link>
                    </li>
                    <li>
                        <Link href="/robot/person-list" onClick={closeMenu}>Suspicious Person</Link>
                    </li>
                    <li>
                        <Link href="/weather" onClick={closeMenu}>Weather</Link>
                    </li>
                </ul>
            </nav>
        </header>
    );
}
