"use client";

import Link from "next/link";


export default function Robot() {
    return (
        <div>
            <h1>Robot</h1>
            <Link href="/person-list">
                <button className="action-button">Detail</button>
            </Link>
        </div>
    )
}