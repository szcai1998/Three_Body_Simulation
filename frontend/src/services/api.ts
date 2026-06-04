import type { SimulationState, Body } from '../store/useSimulationStore'

const API_BASE = 'http://localhost:8000/api'

export const api = {
  async getState(): Promise<SimulationState> {
    const res = await fetch(`${API_BASE}/state`)
    if (!res.ok) throw new Error('Failed to fetch state')
    return res.json()
  },

  async init(preset: string) {
    const res = await fetch(`${API_BASE}/init?preset=${preset}`, { method: 'POST' })
    if (!res.ok) throw new Error('Failed to init')
    return res.json()
  },
  
  async reset() {
    const res = await fetch(`${API_BASE}/reset`, { method: 'POST' })
    if (!res.ok) throw new Error('Failed to reset')
    return res.json()
  },
  
  async getPresets(): Promise<{ presets: string[] }> {
    const res = await fetch(`${API_BASE}/presets`)
    if (!res.ok) throw new Error('Failed to fetch presets')
    return res.json()
  },
  
  async updateConfig(config: Partial<SimulationState>) {
    const res = await fetch(`${API_BASE}/config`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config)
    })
    if (!res.ok) throw new Error('Failed to update config')
    return res.json()
  },

  async addBody(body: Body) {
    const res = await fetch(`${API_BASE}/body`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    })
    if (!res.ok) throw new Error('Failed to add body')
    return res.json()
  },

  async updateBody(bodyId: string, updates: Partial<Body>) {
    const res = await fetch(`${API_BASE}/body/${bodyId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updates)
    })
    if (!res.ok) throw new Error('Failed to update body')
    return res.json()
  },

  async deleteBody(bodyId: string) {
    const res = await fetch(`${API_BASE}/body/${bodyId}`, { method: 'DELETE' })
    if (!res.ok) throw new Error('Failed to delete body')
    return res.json()
  }
}
