/**
 * Vue 3 compatible resize directive to replace vue-resize
 * Provides resize observation functionality for DOM elements
 */

export const vResize = {
  mounted(el, binding) {
    const callback = binding.value;
    
    if (typeof callback !== 'function') {
      console.warn('v-resize directive expects a function as value');
      return;
    }

    // Use ResizeObserver for modern browsers
    if (window.ResizeObserver) {
      const resizeObserver = new ResizeObserver(entries => {
        for (const entry of entries) {
          const { width, height } = entry.contentRect;
          callback({ width, height, target: entry.target });
        }
      });
      
      resizeObserver.observe(el);
      
      // Store observer for cleanup
      el._resizeObserver = resizeObserver;
    } else {
      // Fallback for older browsers
      const resizeHandler = () => {
        const rect = el.getBoundingClientRect();
        callback({ 
          width: rect.width, 
          height: rect.height, 
          target: el 
        });
      };
      
      window.addEventListener('resize', resizeHandler);
      el._resizeHandler = resizeHandler;
    }
  },
  
  unmounted(el) {
    // Cleanup
    if (el._resizeObserver) {
      el._resizeObserver.disconnect();
      delete el._resizeObserver;
    }
    
    if (el._resizeHandler) {
      window.removeEventListener('resize', el._resizeHandler);
      delete el._resizeHandler;
    }
  }
};