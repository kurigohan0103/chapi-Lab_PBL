"use client";

import React, { useEffect, useState } from "react";
import "../../../styles/PersonList.css";

type SuspectImage = {
    id: number;
    suspect_id: number;
    image_url: string; // 画像URL
    captured_at: string;
};

const PersonList = () => {
    const [images, setImages] = useState<SuspectImage[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchImages = async () => {
            try {
                const response = await fetch("http://127.0.0.1:8000/api/suspect_images");
                if (response.ok) {
                    const data = await response.json();
                    setImages(data.images); // `data.images` を使用して状態を更新
                } else {
                    setError("Failed to fetch images");
                }
            } catch (error) {
                setError("Error fetching images");
                console.error("Error fetching images:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchImages();
    }, []);

    if (loading) {
        return <div className="loading-container">Loading...</div>;
    }

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    return (
        <div className="person-list-container">
            <div className="image-grid">
                {images.map((image) => (
                    <div key={image.id} className="image-item">
                        <img
                            src={`http://127.0.0.1:8000${image.image_url}`} // URLを利用して画像を表示
                            className="image-preview"
                        />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PersonList;
