<template>
  <div class="chart-container">
    <chart height="100%" width="100%" />
    <component :is="currentRole" />
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
// import adminDashboard from './admin'
import editorDashboard from './editor'
import Chart from '@/components/Charts/LineMarker'

export default {
  name: 'LineChart',
  components: { Chart, editorDashboard },
  data() {
    return {
      currentRole: 'Chart'
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

<style scoped>
.chart-container{
  position: relative;
  width: 100%;
  height: calc(100vh - 84px);
}
</style>

