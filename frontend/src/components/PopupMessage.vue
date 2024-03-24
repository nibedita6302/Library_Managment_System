<template>
    <div v-if="isVisible" role="alert"
    :class='"alert alert-"+(alert_type? alert_type: "warning")+" fade show text-center"'  >
        <i class="alert-heading">{{ message }}</i><br>
        <button v-if="showCancel" @click="handleCancel" type="button" class="btn btn-outline-dark">
            {{ cancel_text? cancel_text: 'Close' }}
        </button> &nbsp;
        <button v-if="showConfirm" @click="handleConfirm" type="button" class="btn btn-outline-success">
            {{ confirm_text? confirm_text: 'Confirm' }}
        </button>
    </div>
</template>

<script>
export default{
    name: 'PopupMessage',
    props: {
        message: {
            type: String, 
            required: true
        },
        showCancel: {
            type: Boolean, 
            default: true
        },
        cancel_text: {
            type: String,  
            default: 'Close'
        },
        showConfirm: {
            type: Boolean, 
            default: false
        },
        confirm_text: {
            type: String,
            default: 'Confirm'
        },
        alert_type: {
            type: String,
            default: 'warning'
        }
    },
    data() {
        return {
            isVisible: true 
        }
    },
    methods: {
        handleCancel(){
            this.isVisible = false,
            this.$emit('cancel');
        },
        handleConfirm(){
            this.isVisible = false,
            this.$emit('confirm');
        }
    }
}

</script>

<style scoped>
button{
    font-size: small;
}
</style>