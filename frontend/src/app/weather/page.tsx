"use client";

import Link from "next/link";
import Image from "next/image";


export default function Robot() {
    return (
        <div>
            <h1>Weather</h1>
            <Image
                src="/image/rain-icon.png"
                alt="Rain Illustration"
                width={200}
                height={200}
                className="rain-image"
            />
            <h1>雨雲接近中</h1>
            <Link href="/mypage">
                <button className="action-button">Detail</button>
            </Link>
        </div>
    )
}