'use client';

import { Radar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    RadialLinearScale,
    PointElement,
    LineElement,
    Filler,
    Tooltip,
    Legend,
} from 'chart.js';
import type { RadarChartItem } from '../types';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

interface DimensionRadarProps {
    data: RadarChartItem[];
}

export default function DimensionRadar({ data: radarData }: DimensionRadarProps) {
    const dimensions = radarData.map(s => s.dimension);
    const userScores = radarData.map(s => s.user_score);
    const benchmarkScores = radarData.map(s => s.benchmark_score);

    const data = {
        labels: dimensions,
        datasets: [
            {
                label: 'Your Score',
                data: userScores,
                backgroundColor: 'rgba(79, 70, 229, 0.25)', // Increased opacity
                borderColor: '#6366f1', // Indigo 500 (lighter/brighter)
                borderWidth: 3,
                pointBackgroundColor: '#4f46e5',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#4f46e5',
                pointRadius: 5,
                pointHoverRadius: 7,
            },
            {
                label: 'Benchmark',
                data: benchmarkScores,
                backgroundColor: 'rgba(203, 213, 225, 0.2)', // Slate 300 with opacity
                borderColor: '#94a3b8', // Slate 400
                borderWidth: 2,
                borderDash: [5, 5],
                pointRadius: 0,
                pointHoverRadius: 0,
                fill: true,
            },
        ],
    };

    const options = {
        responsive: true,
        maintainAspectRatio: true,
        scales: {
            r: {
                beginAtZero: true,
                max: 100,
                min: 0,
                ticks: {
                    display: false,
                    stepSize: 20,
                },
                grid: {
                    color: '#e2e8f0', // Slate 200
                },
                pointLabels: {
                    color: '#475569', // Slate 600
                    font: {
                        size: 11,
                        weight: 600,
                        family: 'Inter',
                    },
                },
                angleLines: {
                    color: '#e2e8f0',
                },
            },
        },
        plugins: {
            legend: {
                display: false,
            },
            tooltip: {
                backgroundColor: '#0f172a',
                titleColor: '#fff',
                bodyColor: '#e2e8f0',
                padding: 12,
                cornerRadius: 8,
                displayColors: false,
            },
        },
    };

    return (
        <div className="w-full max-w-md mx-auto">
            <Radar data={data} options={options} />
        </div>
    );
}
