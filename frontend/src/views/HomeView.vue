<template>
  <SearchBar/>
  <SectionDisplay></SectionDisplay>
</template>

<script>
import SearchBar from '@/components/SearchBar.vue';
import SectionDisplay from '@/components/SectionDisplay.vue';

export default {
  name: 'HomeView',
  components:{
    SearchBar,
    SectionDisplay
  }
}
</script>

<style scoped>
  
</style>
