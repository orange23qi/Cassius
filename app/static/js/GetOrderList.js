function GetOrderList(OrderType){
    $.ajax({
        type:'GET',
        url:'/workflow/orderlist/' + OrderType,
        dataType:'json',
        success:function (data){
            var OrderList = data.data;
            var $html = '';

            $html += '<thead><tr><th>工单编号</th>';
            $html += '<th>工单名称</th>';
            $html += '<th>工单类型</th>';
            $html += '<th>工单状态</th>';
            $html += '<th>当前处理人</th>';
            $html += '<th>申请人</th>';
            $html += '<th>创建时间</th>';
            $html += '<th></th></tr><thead>';

            for(var i=0;i<OrderList.length;i++){
                $html += '<tr><td>'+OrderList[i][0]+'</td>';
                $html += '<td>'+OrderList[i][1]+'</td>';
                $html += '<td>'+OrderList[i][2]+'</td>';
                $html += '<td>'+OrderList[i][3]+'</td>';
                $html += '<td>'+OrderList[i][4]+'</td>';
                $html += '<td>'+OrderList[i][5]+'</td>';
                $html += '<td>'+OrderList[i][6]+'</td>';
                $html += '<td><input type="button" class="king-btn king-primary pull-right" value="详情"'
                if ( OrderList[i][2] == 'MySql表结构变更' ){
                    suburl = 'mysql/orderdetail/ddl'
                } else if ( OrderList[i][2] == 'MySql数据变更' ){
                    suburl = 'mysql/orderdetail/dml'
                }
                $html += 'onclick="javascript:location.href=\'/workflow/'+suburl
                $html += '/?'+OrderList[i][0]+'\'" /><td></tr>';
            }

            if (OrderList.length == 0 ){
                $html +='<tr><td>当前状态暂无工单.</td><td></td><td></td>'
                $html += '<td></td><td></td><td></td><td></td></tr>';
            }
            
            if ( OrderType == 'todo' ){
                $('.ordertodolist').append($html)
            } else if ( OrderType == 'doing' ){
                $('.orderdoinglist').append($html)
            } else if ( OrderType == 'finish' ){
                $('.orderfinishlist').append($html)
            } else if ( OrderType == 'all' ){
                $('.orderalllist').append($html)
            }
        },
        error:function(XMLHttpRequest, textStatus, errorThrown) {
            alert(errorThrown);
        }
    });
}

GetOrderList('todo');
GetOrderList('doing');
GetOrderList('finish');
GetOrderList('all');
