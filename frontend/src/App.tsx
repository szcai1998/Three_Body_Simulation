import { useEffect } from 'react'
import { SimulationCanvas } from './components/SimulationCanvas'
import { SimulationControls } from './components/SimulationControls'
import { HiddenPanel } from './components/HiddenPanel'
import { simulationWs } from './services/websocket'

function App() {
  // Establish WebSocket connection on mount
  useEffect(() => {
    simulationWs.connect()
    return () => {
      simulationWs.disconnect()
    }
  }, [])

  return (
    <div className="relative w-full h-screen overflow-hidden bg-zinc-950 text-zinc-50 font-sans">
      
      {/* 3D Scene (Underlay) */}
      <SimulationCanvas />
      
      {/* UI Overlay (Pointer events restricted where needed) */}
      <div className="absolute inset-0 pointer-events-none">
        
        {/* Header Title */}
        <div className="absolute top-6 left-6 pointer-events-auto">
          <h1 className="text-2xl font-light tracking-widest text-white/90">
            THREE <span className="font-semibold text-blue-400">BODY</span>
          </h1>
          <p className="text-xs text-zinc-500 tracking-wider mt-1 uppercase">
            Gravitational Dynamics
          </p>
        </div>

        {/* Telemetry Drawer */}
        <div className="pointer-events-auto">
          <HiddenPanel />
        </div>

        {/* Bottom Controls */}
        <div className="pointer-events-auto">
          <SimulationControls />
        </div>

      </div>
    </div>
  )
}

export default App
