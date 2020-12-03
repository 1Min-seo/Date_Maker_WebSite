var submenuItem = {
    props: ['item'],
    template: '<li v-on:click="passItem">{{ item }}</li>',
    methods: {
        passItem: function () {
            console.log(this.item)
            this.$emit('change', this.item)
        },
    }
}
var vm = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {
        items: null,
        selected: '명동',
        selectList: ['광화문', '명동', '동대문', '홍대', '여의도', '이태원', '강남', '잠실']
    },
    components: {
        'submenu-item': submenuItem
    },
    created: function () {
        this.getData(this.selected);
    }
    ,
    methods: {
        changeItem: function (item) {
            this.selected = item
            this.getData(this.selected);
        },
        getData: function (location) {
            var vm = this;
            axios.post(`${window.origin}/datemaker/seoul/places`, {
                title: location
            })
                .then((response) => {
                    responseData = JSON.parse(JSON.stringify(response.data));
                    vm.items = responseData;
                })
                .catch((error) => {
                    console.log(error)
                })
        },
        async addCart(item) {
            try {
                await axios.post(`${window.origin}/datemaker/response/cart`, {
                    number: 1,
                    item: item,
                    section : 'add'
                })
                alert('상품이 데이트바구니에 담겼습니다.')

            } catch (error) {
                if (error.response.status == 403) { //forbidden
                    alert('로그인 해주세요')
                }
            }
            console.log(JSON.parse(JSON.stringify(item)))
        }
    }
})