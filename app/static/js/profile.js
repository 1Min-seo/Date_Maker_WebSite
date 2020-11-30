var vm = new Vue({
    el:"#app",
    delimiters:['${', '}'], 
    data : {
        /*server data */
        colors : [0,0,0,0,0,0,0],
        days : ['Mon','Tue','Wed','Thu','Fri','Set','Sun'],
        /*reset data */
        profile : true,
        date : null,  //양방향으로 바인딩된 데이터 
        names : ['cele1','cele2','cele3','cele4']
        /*server data */


    },
    computed : {
        sendDate : function(){
            if(this.date !== null){
                return this.date.split('-').join('/');
            }else{
                return null 
            }
        },
         
    },
    methods : {
        startProfile : function(){
            this.profile = true;
        },
        classToggle : function(index,event){
          
            let color = this.colors[index]; 
            console.log(event.target.style.backgroundColor);
            console.log(color);
            switch(color){
                case 4:
                    this.colors[index] = 0;
                    event.target.style.backgroundColor = 'green'
                    break;
                case 3:
                    this.colors[index] ++;
               
                    event.target.style.backgroundColor = 'red' 
                    break;
                case 2:
                    this.colors[index] ++; 
                    event.target.style.backgroundColor = 'blue' 
                    break
                case 1:
                    this.colors[index] ++; 
                    event.target.style.backgroundColor = 'white'
                    break;
                case 0:
                    this.colors[index] ++; 
                    event.target.style.backgroundColor = 'dodgerblue'

            }
        } 
     }} );