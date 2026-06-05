import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stars } from '@react-three/drei'
import { EffectComposer, Bloom } from '@react-three/postprocessing'
import { useSimulationStore } from '../store/useSimulationStore'
import { CelestialBody } from './CelestialBody'

export function SimulationCanvas() {
  const bodies = useSimulationStore((state) => state.bodies)
  const shadowBodies = useSimulationStore((state) => state.shadow_bodies)
  const editMode = useSimulationStore((state) => state.editMode)
  
  console.log('Rendering Canvas with bodies:', bodies?.length)

  return (
    <div className="absolute inset-0 w-full h-full pointer-events-auto">
      <Canvas camera={{ position: [0, 0, 15], fov: 45, far: 10000 }}>
        <color attach="background" args={['#050508']} />
        
        <ambientLight intensity={0.2} />
        <Stars radius={5000} depth={500} count={5000} factor={10} saturation={0} fade speed={1} />
        
        {bodies.map(body => (
          <CelestialBody key={body.id} body={body} />
        ))}
        
        {shadowBodies && shadowBodies.map(body => (
          <CelestialBody key={body.id + "_ghost"} body={body} isGhost={true} />
        ))}
        
        <OrbitControls 
          makeDefault 
          enableDamping 
          dampingFactor={0.05} 
          minDistance={1} 
          maxDistance={5000}
          enableRotate={!editMode}
        />
        
        {editMode && (
          <gridHelper args={[100, 100, '#3b82f6', '#1f2937']} position={[0,0,-0.1]} rotation={[Math.PI/2, 0, 0]} />
        )}
        
        <EffectComposer>
          <Bloom 
            luminanceThreshold={0.5} 
            intensity={1.5} 
          />
        </EffectComposer>
      </Canvas>
    </div>
  )
}
