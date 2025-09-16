/**
 * Vue 3 compatible mapFields utility to replace vuex-map-fields
 * Provides two-way data binding between Vuex store and component computed properties
 */

export function mapFields(fields) {
  const result = {};
  
  fields.forEach(field => {
    // Extract the property name from the path (e.g., 'map.plotActive' -> 'plotActive')
    const propertyName = field.split('.').pop();
    
    result[propertyName] = {
      get() {
        return getField(this.$store.state, field);
      },
      set(value) {
        this.$store.commit('updateField', { path: field, value });
      }
    };
  });
  
  return result;
}

/**
 * Utility to get nested field value from state
 */
export function getField(state, path) {
  return path.split('.').reduce((obj, key) => {
    return obj && obj[key];
  }, state);
}

/**
 * Utility to set nested field value in state
 */
export function updateField(state, { path, value }) {
  const keys = path.split('.');
  const lastKey = keys.pop();
  
  const target = keys.reduce((obj, key) => {
    if (!obj[key]) {
      obj[key] = {};
    }
    return obj[key];
  }, state);
  
  target[lastKey] = value;
}