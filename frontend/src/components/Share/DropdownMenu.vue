<template>
  <div :class="{active:isActive}" class="share-dropdown-menu">
    <div class="share-dropdown-menu-wrapper">
      <span class="share-dropdown-menu-title" @click.self="clickTitle">{{ title }}</span>
      <div v-for="(item,index) of items" :key="index" class="share-dropdown-menu-item">
        <a v-if="item.href" :href="getSuitableHref(item.href)" target="_blank">{{ item.title }}</a>
        <span v-else>{{ item.title }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      default: function() {
        return []
      }
    },
    title: {
      type: String,
      default: 'vue'
    },
    defaultActive: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isActive: this.defaultActive
    }
  },
  methods: {
    clickTitle() {
      this.isActive = !this.isActive
    },
    getSuitableHref(href) {
      if (process.env.NODE_ENV === 'development' && href.match('^\/')) {
        href = document.location.protocol + '//' + 'autochemistry.com' + href
      }
      if (href.match('.*\.pdf')) {
        return href + '#page=1&view=FitH,top'
      }
      return href
    }
  }
}
</script>

<style lang="scss" >
$n: 20; //和items.length 相同
$t: .0s;
.share-dropdown-menu {
  width: 250px;
  position: relative;
  z-index: 1;
  &-title {
    width: 100%;
    display: block;
    cursor: pointer;
    background: black;
    color: white;
    height: 60px;
    line-height: 60px;
    font-size: 20px;
    text-align: center;
    z-index: 2;
    transform: translate3d(0,0,0);
  }
  &-wrapper {
    position: relative;
  }
  &-item {
    text-align: center;
    position: absolute;
    width: 80%;
    background: #e0e0e0;
    line-height: 60px;
    height: 60px;
    cursor: pointer;
    font-size: 20px;
    opacity: 1;
    transition: transform 0.21s ease;
    &:hover {
      background: black;
      color: white;
    }
    @for $i from 1 through $n {
      &:nth-of-type(#{$i}) {
        z-index: -1;
        transition-delay: (($i+1)/2)*$t;
        transform: translate3d(0, -60px, 0);
      }
    }
  }
  &.active {
    .share-dropdown-menu-wrapper {
      z-index: 1;
    }
    .share-dropdown-menu-item {
      @for $i from 1 through $n {
        &:nth-of-type(#{$i}) {
         transition-delay: ($n - $i)*$t;
          transform: translate3d(100% * (($i+1)%2), $i / 2 * 60px - (($i + 1) % 2 + 1) * 30px, 0);
        }
      }
    }
  }
}
</style>
