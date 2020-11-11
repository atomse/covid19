<template>
  <div class="app-container documentation-container">
    <!--<a class="document-btn" target="_blank" href="https://panjiachen.github.io/vue-element-admin-site/">{{ $t('documentation.documentation') }}</a>
    <a class="document-btn" target="_blank" href="https://github.com/PanJiaChen/vue-element-admin/">{{ $t('documentation.github') }}</a>
    <a class="document-btn" target="_blank" href="https://panjiachen.gitee.io/vue-element-admin-site/zh/">国内文档</a>
    <dropdown-menu :items="articleList" style="float:left;margin-left:40px;" title="系列文章" />-->
    <dropdown-menu :items="manuals" style="float:left;margin-left:10px;width:200px" title="量子化学软件手册" default-active />
  </div>
</template>

<script>
import DropdownMenu from '@/components/Share/DropdownMenu'

export default {
  name: 'Documentation',
  components: { DropdownMenu },
  data() {
    return {
      isActive: true,
      manuals: [
        { title: 'Gaussian16', href: '/static/manuals/gaussian/gaussian16.pdf' },
        { title: 'GaussView6', href: '/static/manuals/gaussview/gv6.pdf' },
        { title: 'ADF2019', href: '/static/manuals/adf/ADF2019.pdf' },
        { title: 'VASP', href: '/static/manuals/vasp/vasp.pdf' },
        { title: 'ORCA', href: '/static/manuals/orca/orca.pdf' },
        { title: 'CP2K', href: 'https://manual.cp2k.org' },
        { title: 'Pyscf', href: 'https://sunqm.github.io/pyscf/' },
        { title: 'ASE', href: 'https://wiki.fysik.dtu.dk/ase/index.html' },
        { title: 'Molcas', href: '/static/manuals/molcas/molcas.pdf' },
        { title: 'Molpro', href: '/static/manuals/molpro/molpro.pdf' },
        { title: 'NBO7', href: '/static/manuals/nbo/nbo.pdf' },
        { title: 'Crystal', href: '/static/manuals/crystal/crystal.pdf' },
        { title: 'Amber', href: '/static/manuals/amber/amber.pdf' },
        { title: 'AmberTools', href: '/static/manuals/amber/ambertools.pdf' },
        { title: 'NAMD', href: '/static/manuals/namd/namd.pdf' },
        { title: 'Gromacs', href: '/static/manuals/gromacs/gromacs.pdf' },
        { title: 'NWChem', href: '/static/manuals/nwchem/nwchem.pdf' },
        { title: 'VESTA', href: '/static/manuals/vesta/vesta.pdf' },
        { title: 'VMD', href: '/static/manuals/vmd/vmd.pdf' }
      ]
    }
  }
}
</script>

<style lang="scss" scoped>
.documentation-container {
  margin: 40px;
  .document-btn {
    float: left;
    margin-left: 40px;
    display: block;
    cursor: pointer;
    background: black;
    color: white;
    height: 40px;
    width: 200px;
    line-height: 40px;
    font-size: 20px;
    text-align: center;
  }
}
</style>
