const showInfo = {
    props : ['item'],
    template : "<button v-on:click='showInfo'>상세정보 검색하기</button>",
    methods : {
      showInfo : function(){
        this.$emit('show',this.item); 
      }
    },
  }
  var vm = new Vue({
      el:"#app",
      delimiters: ['${', '}'],
      data : {
        // server data 
          items : null,
          logging : null,
          link : null 
      },
      components : {
        'show-info': showInfo
      },
      async created  () {
          var vm = this;
          try{
            const response = await axios.post(`${window.origin}/datemaker/cart/res`)
            vm.items =JSON.parse(JSON.stringify(response.data)); 
            vm.logging= JSON.parse(JSON.stringify(response.data));  
          }catch(error){
            console.log(error);
            if(error.response.status == 404){
              alert('세션이 만기되었습니다.')
              window.location.href = `${window.origin}/`
            }
          }
          setTimeout(function() { //$(this.$el).find('#carousel')
          const dragArea = document.querySelector(".wrapper");
          new Sortable(dragArea, {
            ghostClass : "sortable-ghost",
            animation: 350,
            onUpdate : function(event){
                console.log(event)
                console.log(event.oldIndex)
                console.log(event.newIndex)
                vm.change(event.oldIndex,event.newIndex)
            }
          },500);}) 
      },
      methods : {
        change : function(oldIndex,newIndex){
          var prv = this.logging[oldIndex];
          var cur = this.logging[newIndex];
          this.logging[oldIndex] = cur
          this.logging[newIndex] = prv
          console.log(this.logging)
        },
        showInfo : function(item){
          console.log(item)
          this.link = item[0]
        },
        deleteItem : function(index){
          this.items.splice(index,1)        
        }
        
      }
    
  })
