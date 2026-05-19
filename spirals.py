import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import TextBox
import sys

class PrimeSpiralsAnimator:
    def __init__(self, n_max=20000):
        self.n_max = n_max
        self.current_idx = 0
        self.points_per_frame = 20
        
        # State Flags
        self.is_dark_mode = True
        self.show_grid = False
        self.show_lines = False
        self.show_dots = True
        
        # Colors
        self.bg_dark = '#000000'
        self.bg_light = '#ffffff'
        self.text_dark = '#ffffff'
        self.text_light = '#000000'
        self.color_ulam = '#00ffcc'
        self.color_sacks = '#ff00cc'
        self.color_search = '#ffeb3b'
        self.color_path = '#555555'
        
        print("[*] Precomputing geometrical matrices...")
        self.primes_mask = self._generate_primes_mask(self.n_max)
        self.ux, self.uy = self._compute_ulam(self.n_max)
        self.sx, self.sy = self._compute_sacks(self.n_max)
        
        # Setup Figure and Axes
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(16, 8))
        self.fig.canvas.manager.set_window_title('Interactive Prime Spirals')
        # Mayor espacio en la parte inferior para evitar solapamientos
        self.fig.subplots_adjust(bottom=0.25)
        
        # Inicializar líneas con un solo punto para evitar errores de render inicial
        self.line_ulam, = self.ax1.plot([0], [0], color=self.color_path, linewidth=0.3, zorder=1, alpha=0.0)
        self.line_sacks, = self.ax2.plot([0], [0], color=self.color_path, linewidth=0.3, zorder=1, alpha=0.0)
        
        # Initialize Scatters (Dots) con alpha en 0.9 (visibles por defecto)
        self.scatter_ulam = self.ax1.scatter([], [], s=6, c=self.color_ulam, zorder=2, alpha=0.9)
        self.scatter_sacks = self.ax2.scatter([], [], s=6, c=self.color_sacks, zorder=2, alpha=0.9)
        
        # Search Highlights
        self.highlight_ulam, = self.ax1.plot([], [], 'o', color=self.color_search, markersize=10, zorder=5)
        self.highlight_sacks, = self.ax2.plot([], [], 'o', color=self.color_search, markersize=10, zorder=5)
        
        # Fixed limits
        self.ax1.set_xlim(np.min(self.ux)-2, np.max(self.ux)+2)
        self.ax1.set_ylim(np.min(self.uy)-2, np.max(self.uy)+2)
        self.ax2.set_xlim(np.min(self.sx)-2, np.max(self.sx)+2)
        self.ax2.set_ylim(np.min(self.sy)-2, np.max(self.sy)+2)
        
        # UI Elements: Info Text (Alineado a la izquierda)
        self.info_text = self.fig.text(0.02, 0.05, self._get_status_text(), 
                                       fontsize=10, family='monospace', verticalalignment='bottom')
        
        # UI Elements: Search Box (Movido a la extrema derecha para evitar solapamiento)
        axbox = self.fig.add_axes([0.80, 0.05, 0.15, 0.05])
        self.text_box = TextBox(axbox, 'Search N: ', initial='', color='#ffffff', hovercolor='#e6e6e6')
        self.text_box.on_submit(self.search_number)
        
        self.apply_theme()
        
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        
        print("[+] Starting Live Animation Engine...")
        self.anim = FuncAnimation(self.fig, self.update, interval=16, blit=False, cache_frame_data=False)

    def _generate_primes_mask(self, n):
        mask = np.ones(n, dtype=bool)
        mask[:2] = False
        for i in range(2, int(n**0.5) + 1):
            if mask[i]:
                mask[i*i::i] = False
        return mask

    def _compute_ulam(self, n_points):
        x, y = np.zeros(n_points), np.zeros(n_points)
        dx, dy = 1, 0
        segment_length, segment_passed = 1, 0
        cx, cy = 0, 0
        for i in range(n_points):
            x[i], y[i] = cx, cy
            cx += dx
            cy += dy
            segment_passed += 1
            if segment_passed == segment_length:
                segment_passed = 0
                dx, dy = -dy, dx
                if dy == 0:
                    segment_length += 1
        return x, y

    def _compute_sacks(self, n_points):
        n = np.arange(n_points)
        r = np.sqrt(n)
        theta = 2 * np.pi * np.sqrt(n)
        return r * np.cos(theta), r * np.sin(theta)

    def apply_theme(self):
        bg_col = self.bg_dark if self.is_dark_mode else self.bg_light
        txt_col = self.text_dark if self.is_dark_mode else self.text_light
        
        self.fig.patch.set_facecolor(bg_col)
        for ax in (self.ax1, self.ax2):
            ax.set_facecolor(bg_col)
            ax.tick_params(colors=txt_col)
            for spine in ax.spines.values():
                spine.set_color(txt_col)
                # Ocultar o mostrar los bordes de la gráfica según show_grid
                spine.set_visible(self.show_grid)
        
        self.ax1.set_title('Ulam Spiral', color=txt_col, fontsize=14, pad=10)
        self.ax2.set_title('Sacks Spiral', color=txt_col, fontsize=14, pad=10)
        
        self.info_text.set_color(txt_col)
        self.text_box.label.set_color(txt_col)
        
        # Grid Configuration (Fix del Traceback)
        if self.show_grid:
            self.ax1.grid(True, color=txt_col, alpha=0.15, linestyle='--')
            self.ax2.grid(True, color=txt_col, alpha=0.15, linestyle='--')
            self.ax1.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
            self.ax2.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
        else:
            self.ax1.grid(False)
            self.ax2.grid(False)
            # Ocultamos los ticks en lugar de destruir el array interno
            self.ax1.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
            self.ax2.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
            
        self.fig.canvas.draw_idle()

    def _get_status_text(self):
        return (f"CONTROLS:\n"
                f"[UP/DOWN] Adjust Speed | [B] Toggle Theme | Speed: {self.points_per_frame} pts/frame\n"
                f"[G] Toggle Grid        | [L] Toggle Lines | [C] Toggle Dots\n"
                f"Plotted Index: {min(self.current_idx, self.n_max)} / {self.n_max}")

    def on_key_press(self, event):
        # Ignorar inputs si el cursor está dentro de la caja de texto
        if self.text_box.capturekeystrokes:
            return

        if event.key == 'b':
            self.is_dark_mode = not self.is_dark_mode
            self.apply_theme()
        elif event.key == 'g':
            self.show_grid = not self.show_grid
            self.apply_theme()
        elif event.key == 'l':
            self.show_lines = not self.show_lines
            # Uso de opacidad en lugar de visibilidad para prevenir bloqueos de render
            alpha_val = 0.8 if self.show_lines else 0.0
            self.line_ulam.set_alpha(alpha_val)
            self.line_sacks.set_alpha(alpha_val)
            
            # Inyectamos los datos inmediatamente para evitar un renderizado en blanco al activar
            if self.show_lines:
                idx = min(self.current_idx, self.n_max)
                self.line_ulam.set_data(self.ux[:idx], self.uy[:idx])
                self.line_sacks.set_data(self.sx[:idx], self.sy[:idx])
                
            self.fig.canvas.draw_idle()
        elif event.key == 'c':
            self.show_dots = not self.show_dots
            alpha_val = 0.9 if self.show_dots else 0.0
            self.scatter_ulam.set_alpha(alpha_val)
            self.scatter_sacks.set_alpha(alpha_val)
            self.fig.canvas.draw_idle()
        elif event.key == 'up':
            self.points_per_frame = min(500, self.points_per_frame + 5)
            self.info_text.set_text(self._get_status_text())
        elif event.key == 'down':
            self.points_per_frame = max(1, self.points_per_frame - 5)
            self.info_text.set_text(self._get_status_text())

    def search_number(self, text):
        try:
            val = int(text)
            if 0 <= val < self.n_max:
                self.highlight_ulam.set_data([self.ux[val]], [self.uy[val]])
                self.highlight_sacks.set_data([self.sx[val]], [self.sy[val]])
                
                if val > self.current_idx:
                    self.current_idx = val + 1
            else:
                self.text_box.set_val('Out of bounds')
        except ValueError:
            self.text_box.set_val('Invalid Int')
            
        self.fig.canvas.draw_idle()

    def update(self, frame):
        if self.current_idx < self.n_max:
            self.current_idx += self.points_per_frame
            idx = min(self.current_idx, self.n_max)
            
            # --- CORRECCIÓN AQUÍ: Actualización optimizada ---
            # Solo enviamos vectores al motor de Matplotlib si las líneas están activas (evita el congelamiento)
            if self.show_lines:
                self.line_ulam.set_data(self.ux[:idx], self.uy[:idx])
                self.line_sacks.set_data(self.sx[:idx], self.sy[:idx])
            
            # Update scatter points
            current_primes = self.primes_mask[:idx]
            self.scatter_ulam.set_offsets(np.c_[self.ux[:idx][current_primes], self.uy[:idx][current_primes]])
            self.scatter_sacks.set_offsets(np.c_[self.sx[:idx][current_primes], self.sy[:idx][current_primes]])
            
            self.info_text.set_text(self._get_status_text())
            
        return self.scatter_ulam, self.scatter_sacks, self.line_ulam, self.line_sacks, self.info_text

if __name__ == "__main__":
    app = PrimeSpiralsAnimator(n_max=20000)
    try:
        plt.show()
    except KeyboardInterrupt:
        sys.exit(0)
