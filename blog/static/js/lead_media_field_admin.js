function meSelectOrRemoveMedia(action)
{

    MediaExplorer.div_id='currentImageDiv';
    MediaExplorer.type_input_id='id_lead_media_type';
    MediaExplorer.file_input_id='id_lead_media_id';
    MediaExplorer.caption_input_ids = ["id_lead_media_caption","temp_caption"];
    MediaExplorer.credit_input_ids = ["id_lead_media_credit","temp_credit"];
    MediaExplorer.callback = 'meProcessLeadMedia';
    if ( action == "select" )
    {
        MediaExplorer.openWindow();
    }
    else if ( action == "remove" )
    {
        MediaExplorer.remove();
    }
}

function meProcessLeadMedia()
{

    $("#mediaInfoDiv").html("");
    $("#mediaInfoDiv").hide();
    $("#leadMediaImageDiv").hide();

    var id = $('input[name="lead_media_id"]').val();
    var type = $('input[name="lead_media_type"]').val();

    if ( id && type )
    {
        var url = "/api/media/elements/" + id;

        if ( type == "gallery" )
        {
            url = "/api/media/galleries/" + id;
        }
        else if ( type == "image" )
        {
            $("#leadMediaImageDiv").show();
        }

        $.ajax({
            url: url
        }).done(function(data) {
            var html = "";
            html = "<div>";
            html += "<b>Media name:</b> ";
            if ( type == "image" )
            {
                html += "<a target='_blank' href='" + data.image_url + "'>"
                html += data.name;
                html += "</a>";
            }
            else if ( type == "video" )
            {
                html += "<a target='_blank' href='" + data.video_url + "'>"
                html += data.name;
                html += "</a>";
            }
            else if ( type == "gallery" )
            {
                html += data.name;
            }
            html += "</div>";
            html += "<div>";
            html += "<b>Media type:</b> " + type;
            html += "</div>";
            $("#mediaInfoDiv").html(html);
            $("#mediaInfoDiv").show();

            var html2 = "<img style='max-width:150px' src='";
            html2 += data.thumbnail_image_url;
            html2 += "' >";
            $("#currentImageDiv").html(html2);

        });
    }
}

$(function() {

  if ( $('input[name="lead_media_id"]').length )
  {

    $( '#temp_caption' ).keyup( function() {
      $("#id_lead_media_caption").val($(this).val());
    }); 

    $( '#temp_credit' ).keyup( function() {
      $("#id_lead_media_credit").val($(this).val());
    }); 

    meProcessLeadMedia();

    $("#temp_caption").val($("#id_lead_media_caption").val());
    $("#temp_credit").val($("#id_lead_media_credit").val());

  }


});

