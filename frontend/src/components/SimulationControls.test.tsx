import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import { SimulationControls } from './SimulationControls'
import { useSimulationStore } from '../store/useSimulationStore'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { api } from '../services/api'
import { simulationWs } from '../services/websocket'

// Mock the API and Websocket services
vi.mock('../services/api', () => ({
  api: {
    getPresets: vi.fn().mockResolvedValue({ presets: ['figure8', 'binary_orbit'] }),
    reset: vi.fn().mockResolvedValue({ status: 'ok' }),
    init: vi.fn().mockResolvedValue({ status: 'ok' }),
    updateConfig: vi.fn().mockResolvedValue({ status: 'ok' })
  }
}))

vi.mock('../services/websocket', () => ({
  simulationWs: {
    sendCommand: vi.fn()
  }
}))

describe('SimulationControls Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    useSimulationStore.setState({ 
      running: false, 
      integrator: 'verlet',
      chaos_mode: false,
      playback_speed: 1,
      current_preset: "figure8",
      editMode: false
    })
  })

  it('renders presets from api', async () => {
    render(<SimulationControls />)
    
    // Wait for the mock API to resolve and populate the select
    await waitFor(() => {
      expect(screen.getByText('figure8')).toBeInTheDocument()
      expect(screen.getByText('binary orbit')).toBeInTheDocument()
    })
  })

  it('toggles play/pause via websocket', async () => {
    render(<SimulationControls />)
    
    const playButton = screen.getByTitle('Play')
    fireEvent.click(playButton)
    
    expect(simulationWs.sendCommand).toHaveBeenCalledWith('start')
    
    // Change state to running using act
    act(() => {
      useSimulationStore.setState({ running: true })
    })
    
    const pauseButton = await screen.findByTitle('Pause')
    fireEvent.click(pauseButton)
    
    expect(simulationWs.sendCommand).toHaveBeenCalledWith('pause')
  })

  it('toggles chaos mode via API', () => {
    render(<SimulationControls />)
    
    const chaosButton = screen.getByTitle('Toggle Chaos Mode (Perturbation)')
    fireEvent.click(chaosButton)
    
    expect(api.updateConfig).toHaveBeenCalledWith({ chaos_mode: true })
  })
})
