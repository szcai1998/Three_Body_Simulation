import { useEffect, useState } from 'react'
import { Play, Pause, RotateCcw, Settings2, Shuffle, PenTool } from 'lucide-react'
import { useSimulationStore } from '../store/useSimulationStore'
import { simulationWs } from '../services/websocket'
import { api } from '../services/api'

export function SimulationControls() {

  const { running, mode, integrator, chaos_mode, playbackSpeed, editMode, setEditMode } = useSimulationStore()
  const [presets, setPresets] = useState<string[]>([])
  const [currentPreset, setCurrentPreset] = useState("figure8")

  useEffect(() => {
    api.getPresets().then(res => {
      setPresets(res.presets)
    }).catch(err => console.error("Failed to load presets", err))
  }, [])

  const handlePlayPause = () => {
    simulationWs.sendCommand(running ? 'pause' : 'start')
  }

  const handleReset = async () => {
    await api.reset()
  }

  const handlePresetChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const p = e.target.value
    setCurrentPreset(p)
    await api.init(p)
  }

  const handleIntegratorChange = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    await api.updateConfig({ integrator: e.target.value as any })
  }

  return (
    <div className="absolute bottom-6 left-1/2 -translate-x-1/2 glass-panel px-6 py-4 flex items-center space-x-6 text-sm">
      
      {/* Presets */}
      <div className="flex items-center space-x-2 text-zinc-300">
        <span className="font-medium uppercase tracking-wider text-xs text-zinc-400">Preset</span>
        <select 
          value={currentPreset}
          onChange={handlePresetChange}
          className="bg-zinc-900 border border-zinc-700 rounded px-2 py-1 text-white focus:ring-0 cursor-pointer outline-none capitalize"
          aria-label="Select Preset"
        >
          {presets.map(p => (
            <option key={p} value={p}>{p.replace(/_/g, ' ')}</option>
          ))}
        </select>
      </div>

      <div className="w-px h-8 bg-zinc-700/50"></div>

      {/* Playback Controls */}
      <div className="flex items-center space-x-4">
        <button 
          onClick={handleReset}
          className="p-2 hover:bg-white/10 rounded-full transition-colors text-zinc-300 hover:text-white"
          title="Reset Simulation"
          aria-label="Reset Simulation"
        >
          <RotateCcw size={20} />
        </button>
        <button 
          onClick={() => setEditMode(!editMode)}
          className={`p-2 rounded-full transition-colors ${editMode ? 'bg-fuchsia-500/20 text-fuchsia-400' : 'hover:bg-white/10 text-zinc-300 hover:text-white'}`}
          title="Toggle Edit Mode"
          aria-label="Toggle Edit Mode"
        >
          <PenTool size={20} />
        </button>
        <button 
          onClick={handlePlayPause}
          className="p-3 bg-blue-600 hover:bg-blue-500 rounded-full transition-colors text-white shadow-[0_0_15px_rgba(37,99,235,0.5)]"
          title={running ? 'Pause' : 'Play'}
          aria-label={running ? 'Pause' : 'Play'}
        >
          {running ? <Pause size={24} /> : <Play size={24} className="ml-1" />}
        </button>
      </div>

      <div className="w-px h-8 bg-zinc-700/50"></div>

      {/* Settings */}
      <div className="flex items-center space-x-4 text-zinc-300">
        <div className="flex items-center space-x-2">
          <Settings2 size={16} />
          <span className="font-medium uppercase tracking-wider text-xs text-zinc-400">Solver</span>
          <select 
            value={integrator} 
            onChange={handleIntegratorChange}
            className="bg-transparent border-none text-white focus:ring-0 cursor-pointer outline-none"
            aria-label="Select Solver"
          >
            <option value="verlet" className="bg-zinc-900">Velocity Verlet</option>
            <option value="rk4" className="bg-zinc-900">Runge-Kutta 4</option>
            <option value="euler" className="bg-zinc-900">Euler</option>
            <option value="kepler" className="bg-zinc-900" disabled={mode > 2}>Exact Kepler</option>
          </select>
        </div>

        <div className="flex items-center space-x-2">
          <span className="font-medium uppercase tracking-wider text-xs text-zinc-400">Speed</span>
          <select 
            value={playbackSpeed} 
            onChange={(e) => api.updateConfig({ playback_speed: parseInt(e.target.value) })}
            className="bg-transparent border-none text-white focus:ring-0 cursor-pointer outline-none"
            aria-label="Select Playback Speed"
          >
            <option value="1" className="bg-zinc-900">1x</option>
            <option value="2" className="bg-zinc-900">2x</option>
            <option value="5" className="bg-zinc-900">5x</option>
            <option value="10" className="bg-zinc-900">10x</option>
          </select>
        </div>

        <button 
          onClick={() => api.updateConfig({ chaos_mode: !chaos_mode })}
          className={`flex items-center space-x-1 px-3 py-1 rounded transition-colors border ${chaos_mode ? 'bg-red-500/20 border-red-500/50 text-red-400' : 'bg-transparent border-zinc-700 text-zinc-500 hover:text-zinc-300'}`}
          title="Toggle Chaos Mode (Perturbation)"
          aria-label="Toggle Chaos Mode"
        >
          <Shuffle size={14} />
          <span className="text-xs uppercase font-bold">Chaos</span>
        </button>
      </div>
      
    </div>
  )
}
