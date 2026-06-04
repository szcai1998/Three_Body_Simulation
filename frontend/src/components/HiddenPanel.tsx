import { useState } from 'react'
import { Activity, ChevronRight, Zap, Target, Gauge } from 'lucide-react'
import { useSimulationStore } from '../store/useSimulationStore'
import { LineChart, Line, YAxis, ResponsiveContainer } from 'recharts'

export function HiddenPanel() {
  const [isOpen, setIsOpen] = useState(false)
  
  const { 
    energy_drift, 
    angular_momentum, 
    center_of_mass, 
    connected,
    chartData
  } = useSimulationStore()

  const formatSci = (num: number) => num.toExponential(3)
  const formatNum = (num: number) => num.toFixed(4)

  const driftAbs = Math.abs(energy_drift)
  const driftColor = driftAbs < 0.01 ? 'text-green-400' : driftAbs < 0.05 ? 'text-yellow-400' : 'text-red-400'

  return (
    <div className={`absolute top-6 right-0 transition-transform duration-300 ease-in-out ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>
      
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="absolute -left-12 top-0 p-2 glass-panel rounded-r-none rounded-l-md text-zinc-400 hover:text-white border-r-0 flex flex-col items-center justify-center space-y-1"
      >
        <Activity size={20} className={connected ? "text-green-400" : "text-red-400"} />
        <ChevronRight size={16} className={`transition-transform ${isOpen ? '' : 'rotate-180'}`} />
      </button>

      <div className="glass-panel w-80 min-h-64 mr-6 p-4 border-r-0 rounded-r-none rounded-l-lg text-sm text-zinc-300">
        <h2 className="text-white font-semibold uppercase tracking-wider flex items-center space-x-2 mb-4">
          <Activity size={18} className="text-blue-400" />
          <span>Telemetry</span>
        </h2>

        <div className="space-y-4">
          <div className="space-y-1">
            <div className="flex items-center space-x-2 text-zinc-400 text-xs uppercase tracking-wider">
              <Zap size={14} />
              <span>Energy Drift (%)</span>
            </div>
            
            <div className="h-24 w-full mt-2 mb-2 bg-black/20 rounded p-1">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <YAxis domain={['auto', 'auto']} hide />
                  <Line 
                    type="monotone" 
                    dataKey="drift" 
                    stroke={driftAbs < 0.01 ? '#4ade80' : driftAbs < 0.05 ? '#facc15' : '#f87171'} 
                    strokeWidth={2} 
                    dot={false}
                    isAnimationActive={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            
            <div className="flex justify-between font-mono bg-black/20 p-2 rounded">
              <span>Current Drift:</span>
              <span className={driftColor}>{(energy_drift * 100).toFixed(4)}%</span>
            </div>
          </div>

          <div className="space-y-1 mt-4">
            <div className="flex items-center space-x-2 text-zinc-400 text-xs uppercase tracking-wider">
              <Gauge size={14} />
              <span>Kinematics</span>
            </div>
            <div className="flex justify-between font-mono bg-black/20 p-2 rounded">
              <span>Ang. Mom. |L|:</span>
              <span>
                {formatSci(Math.sqrt(angular_momentum.components[0]**2 + angular_momentum.components[1]**2 + angular_momentum.components[2]**2))}
              </span>
            </div>
            <div className="flex justify-between font-mono bg-black/20 p-2 rounded text-xs text-zinc-400">
              <span>COM X: {formatNum(center_of_mass.components[0])}</span>
              <span>Y: {formatNum(center_of_mass.components[1])}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
