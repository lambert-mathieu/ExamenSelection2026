import { Preset } from '../../common/types/Preset';
import * as fs from 'fs';
import * as path from 'path';

interface DatabaseData {
    presets: Preset[];
    user_settings: any[];
    performance_logs: any[];
    compositions: any[];
}

class PresetService {
    private presets: Preset[] = [];
    private dataPath: string;

    constructor() {
        const dbPath = 'data/database.json';
        this.dataPath = path.resolve(__dirname, '..', dbPath);
        this.loadPresets();
    }

    private loadPresets(): void {
        try {
            const data = fs.readFileSync(this.dataPath, 'utf-8');
            const database: DatabaseData = JSON.parse(data);
            this.presets = database.presets;
            console.log(`Loaded ${this.presets.length} presets from ${this.dataPath}`);
        } catch (error) {
            console.error('Error loading presets:', error);
            this.presets = [];
        }
    }

    private savePresets(): void {
        try {
            const data = fs.readFileSync(this.dataPath, 'utf-8');
            const database: DatabaseData = JSON.parse(data);
            database.presets = this.presets;
            fs.writeFileSync(this.dataPath, JSON.stringify(database, null, 2), 'utf-8');
            console.log(`Saved ${this.presets.length} presets to ${this.dataPath}`);
        } catch (error) {
            console.error('Error saving presets:', error);
        }
    }

    public getPresetById(id: number): Preset | undefined {
        return this.presets.find(preset => preset.id === id);
    }

    public getAllPresets(): Preset[] {
        return this.presets;
    }

    public getPresetCount(): number {
        return this.presets.length;
    }

    public getAvailableIds(): number[] {
        return this.presets.map(preset => preset.id);
    }

    public addPreset(preset: Preset): void {
        this.presets.push(preset);
        this.savePresets();
    }

    public updatePreset(id: number, updatedPreset: Partial<Preset>): boolean {
        const index = this.presets.findIndex(preset => preset.id === id);
        if (index === -1) {
            return false;
        }
        this.presets[index] = { ...this.presets[index], ...updatedPreset };
        this.savePresets();
        return true;
    }

    public deletePreset(id: number): boolean {
        const index = this.presets.findIndex(preset => preset.id === id);
        if (index === -1) {
            return false;
        }
        this.presets.splice(index, 1);
        this.savePresets();
        return true;
    }
}

export const presetService = new PresetService();
