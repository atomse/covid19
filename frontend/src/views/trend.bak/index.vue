<template>
  <div class="dashboard-container">
    <component :is="currentRole" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import TrendIndex from './admin'
import editorDashboard from './editor'

export default {
  name: 'Dashboard',
  components: { TrendIndex, editorDashboard },
  data() {
    return {
      currentRole: 'TrendIndex'
    }
  },
  computed: {
    ...mapGetters([
      'roles'
    ])
  },
  created() {
    if (!this.roles.includes('admin')) {
      this.currentRole = 'editorDashboard'
    }
  }
}
</script>
