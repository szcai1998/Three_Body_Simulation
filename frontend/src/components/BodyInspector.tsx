import { useState, useEffect } from 'react'
import { X, SlidersHorizontal } from 'lucide-react'
import { useSimulationStore } from '../store/useSimulationStore'
import { api } from '../services/api'

export function BodyInspector() {
  const { selectedBodyId, bodies, setSelectedBodyId, running } = useSimulationStore()
  
  const body = bodies.find(b => b.id === selectedBodyId)
  
  // Local state for smooth slider dragging before sending to API
  const [localMass, setLocalMass] = useState<number>(1.0)
  
  useEffect(() => {
    if (body) {
      setLocalMass(body.mass)
    }
  }, [body?.id])
  
  if (!body) {
    return null
  }

  const handleMassChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newMass = parseFloat(e.target.value)
    setLocalMass(newMass)
  }

  const handleMassCommit = async () => {
    if (body.id && localMass !== body.mass) {
      await api.updateBody(body.id, { mass: localMass })
    }
  }
  
  const handleVectorChange = async (type: 'position' | 'velocity', axis: 0|1|2, value: string) => {
    const num = parseFloat(value)
    if (isNaN(num)) return
    
    const current = body[type].components
    const newComponents = [...current] as [number, number, number]
    newComponents[axis] = num
    
    await api.updateBody(body.id, {
      [type]: { components: newComponents }
    })
  }

  const formatNum = (n: number) => n.toFixed(3)

  return (
    <div className="absolute top-24 left-6 w-80 glass-panel p-4 rounded-lg text-sm text-zinc-300">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-white font-semibold uppercase tracking-wider flex items-center space-x-2">
          <SlidersHorizontal size={18} className="text-blue-400" />
          <span>Inspector: {body.id}</span>
        </h2>
        <button 
          onClick={() => setSelectedBodyId(null)}
          className="p-1 hover:bg-white/10 rounded-full transition-colors text-zinc-400 hover:text-white"
          aria-label="Close Inspector"
        >
          <X size={16} />
        </button>
      </div>

      <div className="space-y-6">
        
        {/* Mass Control */}
        <div className="space-y-2">
          <div className="flex justify-between items-center text-xs uppercase tracking-wider text-zinc-400">
            <span>Mass</span>
            <span className="font-mono text-blue-400">{localMass.toFixed(2)}</span>
          </div>
          <input 
            type="range" 
            min="0.1" 
            max="10.0" 
            step="0.1"
            value={localMass}
            onChange={handleMassChange}
            onMouseUp={handleMassCommit}
            onTouchEnd={handleMassCommit}
            disabled={running}
            className={`w-full accent-blue-500 h-1 rounded-lg appearance-none cursor-pointer ${running ? 'bg-zinc-800 opacity-50' : 'bg-zinc-700'}`}
            aria-label={`Adjust mass for ${body.id}`}
          />
        </div>

        {/* Position Control */}
        <div className="space-y-2">
          <div className="text-xs uppercase tracking-wider text-zinc-400">Position</div>
          <div className="grid grid-cols-3 gap-2">
            {[0, 1, 2].map(axis => (
              <div key={`pos-${axis}`} className="flex flex-col space-y-1">
                <span className="text-[10px] text-zinc-500">{['X', 'Y', 'Z'][axis]}</span>
                <input 
                  type="number" 
                  step="0.1"
                  value={formatNum(body.position.components[axis as 0|1|2])}
                  onChange={(e) => handleVectorChange('position', axis as 0|1|2, e.target.value)}
                  disabled={running}
                  className={`bg-black/30 border rounded px-2 py-1 text-white font-mono text-xs focus:outline-none ${running ? 'border-zinc-800 text-zinc-500' : 'border-zinc-700/50 focus:border-blue-500'}`}
                  aria-label={`Position ${['X', 'Y', 'Z'][axis]}`}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Velocity Control */}
        <div className="space-y-2">
          <div className="text-xs uppercase tracking-wider text-zinc-400">Velocity</div>
          <div className="grid grid-cols-3 gap-2">
            {[0, 1, 2].map(axis => (
              <div key={`vel-${axis}`} className="flex flex-col space-y-1">
                <span className="text-[10px] text-zinc-500">V{['x', 'y', 'z'][axis]}</span>
                <input 
                  type="number" 
                  step="0.1"
                  value={formatNum(body.velocity.components[axis as 0|1|2])}
                  onChange={(e) => handleVectorChange('velocity', axis as 0|1|2, e.target.value)}
                  disabled={running}
                  className={`bg-black/30 border rounded px-2 py-1 text-white font-mono text-xs focus:outline-none ${running ? 'border-zinc-800 text-zinc-500' : 'border-zinc-700/50 focus:border-blue-500'}`}
                  aria-label={`Velocity ${['X', 'Y', 'Z'][axis]}`}
                />
              </div>
            ))}
          </div>
        </div>
        
        {running && (
          <div className="text-[10px] text-yellow-500 mt-4 text-center bg-yellow-500/10 p-1 rounded">
            Pause simulation to edit body properties.
          </div>
        )}
        
      </div>
    </div>
  )
}
