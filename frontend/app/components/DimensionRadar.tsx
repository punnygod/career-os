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
import type { DimensionScore } from '../types';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, Tooltip, Legend);

interface DimensionRadarProps {
    scores: DimensionScore[];
}

export default function DimensionRadar({ scores }: DimensionRadarProps) {
    const dimensions = scores.map(s => s.dimension);
    const values = scores.map(s => s.score);

    const data = {
        labels: dimensions,
        datasets: [
            {
                label: 'Score',
                data: values,
                backgroundColor: 'rgba(79, 70, 229, 0.1)', // Indigo 600 with opacity
                borderColor: '#4f46e5', // Indigo 600
                borderWidth: 2,
                pointBackgroundColor: '#4f46e5',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#4f46e5',
                pointRadius: 4,
                pointHoverRadius: 6,
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
