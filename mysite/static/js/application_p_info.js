

// application process ---- Resume upload
( function( $, window, document, undefined )
{

$( '.inputfile' ).each( function()
{
	var $input	 = $( this ),
		$label	 = $input.next( 'label' ),
		labelVal = $label.html();

	$input.on( 'change', function( e )
	{
      var fileName = '';
      
      if( e.target.value )
			fileName = e.target.value.split( '\\' ).pop();

		if( fileName )
			$label.find( 'span' ).html( fileName );
		else
			$label.html( labelVal );
	});

	// Firefox bug fix
	$input
	.on( 'focus', function(){ $input.addClass( 'has-focus' ); })
	.on( 'blur', function(){ $input.removeClass( 'has-focus' ); });
});


})( jQuery, window, document );



// application process ---- Image upload
function readURL(input) {
   if (input.files && input.files[0]) {
       var reader = new FileReader();

       reader.onload = function (e) {
           $('#blah')
               .attr('src', e.target.result);
       };

       reader.readAsDataURL(input.files[0]);
   }
}


// handle form submition
