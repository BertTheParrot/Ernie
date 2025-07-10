import pygame
import os
import random
from typing import Dict, List, Optional

class SoundManager:
    """Manages all game audio including sound effects and music"""
    
    def __init__(self, sounds_dir: str = "sounds"):
        self.sounds_dir = sounds_dir
        self.sound_cache: Dict[str, pygame.mixer.Sound] = {}
        self.volume = 0.7
        
        # Initialize pygame mixer with better quality
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Create sounds directory structure
        os.makedirs(self.sounds_dir, exist_ok=True)
        os.makedirs(os.path.join(self.sounds_dir, "animals"), exist_ok=True)
        
        # Animal sound mappings - these will look for real audio files first
        self.animal_sounds = {
            'cow': ['cow_moo1', 'cow_moo2', 'cow_moo3'],
            'pig': ['pig_oink1', 'pig_oink2', 'pig_snort'],
            'chicken': ['chicken_cluck1', 'chicken_cluck2', 'chicken_bawk'],
            'sheep': ['sheep_baa1', 'sheep_baa2'],
            'horse': ['horse_neigh1', 'horse_whinny'],
            'goat': ['goat_bleat1', 'goat_maa']
        }
        
        # Supported audio formats
        self.supported_formats = ['.wav', '.ogg', '.mp3']
        
        # Load real audio files first, then create procedural fallbacks
        self.load_sound_files()
        self.create_procedural_sounds()
    
    def load_sound_files(self) -> None:
        """Load real sound files from the sounds directory"""
        animals_dir = os.path.join(self.sounds_dir, "animals")
        
        print("🎵 Loading sound files...")
        
        # Look for sound files in the animals directory
        for animal_type, sound_names in self.animal_sounds.items():
            for sound_name in sound_names:
                # Check each supported format
                for ext in self.supported_formats:
                    sound_path = os.path.join(animals_dir, f"{sound_name}{ext}")
                    if os.path.exists(sound_path):
                        try:
                            sound = pygame.mixer.Sound(sound_path)
                            self.sound_cache[sound_name] = sound
                            print(f"  ✅ Loaded: {sound_name}{ext}")
                            break  # Found a file, don't check other formats
                        except pygame.error as e:
                            print(f"  ❌ Failed to load {sound_name}{ext}: {e}")
        
        # Also check for generic filenames (like "cow.wav", "chicken.wav")
        for animal_type in self.animal_sounds.keys():
            for ext in self.supported_formats:
                generic_path = os.path.join(animals_dir, f"{animal_type}{ext}")
                if os.path.exists(generic_path):
                    try:
                        sound = pygame.mixer.Sound(generic_path)
                        # Use this sound for all variations of this animal if no specific sounds exist
                        for sound_name in self.animal_sounds[animal_type]:
                            if sound_name not in self.sound_cache:
                                self.sound_cache[sound_name] = sound
                        print(f"  ✅ Loaded generic: {animal_type}{ext}")
                        break
                    except pygame.error as e:
                        print(f"  ❌ Failed to load {animal_type}{ext}: {e}")
    
    def create_procedural_sounds(self) -> None:
        """Create simple procedural animal sounds using pygame"""
        # Create animal sounds if they don't exist
        for animal_type, sound_names in self.animal_sounds.items():
            for sound_name in sound_names:
                sound_path = os.path.join(self.sounds_dir, f"{sound_name}.wav")
                if not os.path.exists(sound_path):
                    try:
                        # Generate a simple sound for this animal
                        sound_data = self._generate_animal_sound(animal_type, sound_name)
                        if sound_data:
                            # Try to create sound from raw audio data
                            # Create a temporary file for pygame to load
                            import tempfile
                            import wave
                            
                            # Create a temporary WAV file
                            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                                with wave.open(tmp_file.name, 'wb') as wav_file:
                                    wav_file.setnchannels(1)  # Mono
                                    wav_file.setsampwidth(2)  # 16-bit
                                    wav_file.setframerate(22050)  # Sample rate
                                    wav_file.writeframes(sound_data)
                                
                                # Load the temporary file
                                sound = pygame.mixer.Sound(tmp_file.name)
                                self.sound_cache[sound_name] = sound
                                
                                # Clean up temp file
                                os.unlink(tmp_file.name)
                    except Exception as e:
                        print(f"Warning: Could not create sound for {sound_name}: {e}")
                        # Create a simple fallback beep
                        self._create_simple_fallback_sound(sound_name, animal_type)
    
    def _generate_animal_sound(self, animal_type: str, sound_name: str) -> Optional[bytes]:
        """Generate simple procedural animal sounds"""
        try:
            import numpy as np
            
            # Sound parameters
            sample_rate = 22050
            duration = 0.5  # seconds
            
            if animal_type == 'chicken':
                # High-pitched quick chirp
                frequency = 800 + random.randint(-100, 200)
                t = np.linspace(0, duration * 0.3, int(sample_rate * duration * 0.3))
                wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 8)
                
            elif animal_type == 'cow':
                # Low-pitched moo
                frequency = 180 + random.randint(-30, 30)
                t = np.linspace(0, duration * 0.8, int(sample_rate * duration * 0.8))
                wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 2)
                
            elif animal_type == 'pig':
                # Snorty oink
                frequency = 300 + random.randint(-50, 100)
                t = np.linspace(0, duration * 0.4, int(sample_rate * duration * 0.4))
                wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 5)
                # Add some noise for snort effect
                noise = np.random.normal(0, 0.1, len(wave))
                wave = wave + noise
                
            elif animal_type == 'sheep':
                # Bleating baa
                frequency = 400 + random.randint(-50, 50)
                t = np.linspace(0, duration * 0.6, int(sample_rate * duration * 0.6))
                wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 3)
                
            elif animal_type == 'horse':
                # Neigh/whinny
                frequency = 500 + random.randint(-100, 100)
                t = np.linspace(0, duration, int(sample_rate * duration))
                wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 2)
                
            elif animal_type == 'goat':
                # Goat bleat
                frequency = 450 + random.randint(-50, 50)
                t = np.linspace(0, duration * 0.5, int(sample_rate * duration * 0.5))
                wave = np.sin(2 * np.pi * frequency * t) * np.exp(-t * 4)
                
            else:
                return None
            
            # Normalize and convert to 16-bit PCM
            wave = np.clip(wave, -1.0, 1.0)
            wave = (wave * 32767).astype(np.int16)
            
            # Convert to bytes
            return wave.tobytes()
            
        except ImportError:
            # If numpy not available, create simple beep
            return self._create_simple_beep(animal_type)
    
    def _create_simple_beep(self, animal_type: str) -> bytes:
        """Create a simple beep sound without numpy"""
        import math
        
        sample_rate = 22050
        duration = 0.3
        
        # Different frequencies for different animals
        freq_map = {
            'chicken': 800,
            'cow': 180,
            'pig': 300,
            'sheep': 400,
            'horse': 500,
            'goat': 450
        }
        
        frequency = freq_map.get(animal_type, 440)
        
        # Generate simple sine wave
        samples = []
        for i in range(int(sample_rate * duration)):
            t = i / sample_rate
            amplitude = 0.5 * math.exp(-t * 3)  # Decay envelope
            sample = amplitude * math.sin(2 * math.pi * frequency * t)
            samples.append(int(sample * 32767))
        
        # Convert to bytes (16-bit signed, little endian)
        try:
            sound_data = b''.join(sample.to_bytes(2, 'little', signed=True) for sample in samples)
            return sound_data
        except (ValueError, OverflowError):
            # If conversion fails, return empty bytes
            return b''
    
    def play_animal_sound(self, animal_type: str) -> None:
        """Play a random sound for the specified animal type"""
        if animal_type in self.animal_sounds:
            sound_names = self.animal_sounds[animal_type]
            sound_name = random.choice(sound_names)
            
            # Try to play from cache first
            if sound_name in self.sound_cache:
                sound = self.sound_cache[sound_name]
                sound.set_volume(self.volume)
                sound.play()
                return
            
            # Try to load from file
            sound_path = os.path.join(self.sounds_dir, f"{sound_name}.wav")
            if os.path.exists(sound_path):
                try:
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(self.volume)
                    sound.play()
                    self.sound_cache[sound_name] = sound
                except pygame.error:
                    print(f"Warning: Could not play sound {sound_path}")
    
    def play_sound(self, sound_name: str) -> None:
        """Play a specific sound by name"""
        if sound_name in self.sound_cache:
            sound = self.sound_cache[sound_name]
            sound.set_volume(self.volume)
            sound.play()
    
    def set_volume(self, volume: float) -> None:
        """Set the overall volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
    
    def _create_simple_fallback_sound(self, sound_name: str, animal_type: str) -> None:
        """Create a very simple fallback sound using pygame primitives"""
        # Create a very short duration sound buffer
        duration = 0.2  # 200ms
        sample_rate = 22050
        samples = int(duration * sample_rate)
        
        # Create a simple array of silence (we'll just skip sound creation for now)
        # This is a fallback for when sound generation fails
        print(f"Using silent fallback for {sound_name}")
        
    def stop_all_sounds(self) -> None:
        """Stop all currently playing sounds"""
        pygame.mixer.stop() 