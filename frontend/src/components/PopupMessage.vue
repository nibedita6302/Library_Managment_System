<template>
    <div v-if="isVisible" class="alert alert-warning fade show text-center" role="alert" >
        <h5 class="alert-heading">{{ message }}</h5>
        <button v-if="showCancel" @click="handleCancel" type="button" class="btn btn-secondary">
            {{ cancel_text }}
        </button> &nbsp;
        <button v-if="showConfirm" @click="handleConfirm" type="button" class="btn btn-success">
            {{ confirm_text }}
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

</style>