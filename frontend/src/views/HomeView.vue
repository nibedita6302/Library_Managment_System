<template>
  <PopupMessage v-if="showPopup"
        message="This is a demo popup. Some more random text!! Alert!!"
        showConfirm="confirm"
        confirm_text="Confirm Button"
        @cancel="handleCancel"
        @confirm="handleConfirm"></PopupMessage>
  <!-- <SearchBar></SearchBar> -->
  <!-- <Category></Category> -->
  <h1>This is Home View Page</h1>
  <button @click="demoPop">Show pop-up</button>
</template>

<script>
// import {mapGetters, mapMutations, mapState} from 'vuex';
import PopupMessage from '@/components/PopupMessage.vue'

export default {
  name: 'HomeView',
  components:{
    PopupMessage,
  },
  data(){
    return {
      showPopup: false,
      confirm: true
    }
  },

  methods:{
    demoPop(){
      if (this.showPopup==false){
        this.showPopup=true;
      }
    },
    handleCancel(){
      this.showPopup = false;
      console.log('cancel');
    },
    handleConfirm(){
      this.showPopup = false;
      console.log('confirm');
    }
  }
  // computed: {
  //   ...mapState('searching',['showProducts']),
  //   ...mapGetters('auth',['GET_USER_ROLE']),
  // }
}
</script>

<style scoped>
  
</style>
