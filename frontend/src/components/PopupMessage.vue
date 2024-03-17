<template>
    <div v-if="isVisible" class="popup-message">
        <div class="popup-content">
            <p>{{ message }}</p>
            <div v-if="showCancel">
                <button @click="handleCancle">{{ cancel_text }}</button>
            </div>
            <div v-if="showConfirm">
                <button @click="handleConfirm">{{ confirm_text }}</button>
            </div>
        </div>
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
            required: false
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
        handleCancle(){
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

.popup-message{
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: white;
    border: 1px solid black;
    padding: 20px;
}
.popup-content{
    display: flex;
    flex-direction: column;
}

</style>