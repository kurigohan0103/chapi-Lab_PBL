"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import "../../styles/Robot.css";

const RobotPage = () => {
    const [securityMode, setSecurityMode] = useState(false);
    const router = useRouter();

    useEffect(() => {
        const fetchSecurityMode = async () => {
            try {
                const response = await fetch("/api/security_mode");
                if (response.ok) {
                    const data = await response.json();
                    setSecurityMode(data.mode);
                } else {
                    console.error("Failed to fetch security mode");
                }
            } catch (error) {
                console.error("Error fetching security mode:", error);
            }
        };

        fetchSecurityMode();
    }, []);

    const handleButtonClick = () => {
        router.push("/robot/person-list");
    };

    return (
        <div className="container">
            {/* 映像ボックス */}
            <div className="cameraContainer">
                {securityMode ? (
                    <img
                        src="http://127.0.0.1:8000/api/video_feed_with_detection"
                        alt="Camera Stream"
                        className="cameraStream"
                    />
                ) : (
                    <div className="placeholder"></div> // 灰色のプレースホルダー
                )}
            </div>

            {/* ボタン */}
            <div className="buttonContainer">
                <button className="button" onClick={handleButtonClick}>
                    List
                </button>
            </div>
        </div>
    );
};

export default RobotPage;
