import React, { useState } from 'react';
import { Note } from '../types/Notes';
import { audioService } from '../services/AudioService';
import { Preset } from '../../../common/types/Preset';
import '../styles/Keyboard.css';

interface KeyboardProps {
    params: Preset;
    startOctave?: number;
    octaveCount?: number;
}

interface KeyInfo {
    name: string;
    note: Note;
    isBlack: boolean;
}

const Keyboard: React.FC<KeyboardProps> = ({
    params,
    startOctave = 4,
    octaveCount = 4,
}) => {
    const [activeKeys, setActiveKeys] = useState<Set<string>>(new Set());

    const octaves = [];
    for (let i = 0; i < octaveCount; i++) {
        const keys = [];
        for (let i = 0; i < 12; i++) {
            keys.push(<div className="key-white"></div>);
        }
        octaves.push(<div className="octave-group">{keys}</div>);
    }

    // seasons.forEach((season, index) => {
    //     seasonsList.push(<li key={index}>{season}</li>);
    // });

    return (
        <div className="keyboard-container">
            <h3>Keyboard - Octaves {startOctave} to {startOctave + octaveCount - 1}</h3>
            {octaves}
        </div>
    );
};

export default Keyboard;
