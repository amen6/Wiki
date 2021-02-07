<input class="form-control" type="text" name="title" style='height: 30px; width:25%;' placeholder="Insert Title">
<textarea class="form-control" name="text" style='height: 300px; width:80%; margin-top: 3px' placeholder="Write Your Page Content HERE"></textarea>

/*
title = request.POST.get('title')
    text = request.POST.get('text')
    if not text or not title:
        messages.error(request, 'Please Insert title and text')
    elif util.get_entry(title):
        messages.error(request, 'Title already exist')
    util.save_entry(title,text)
    return render(request, 'encyclopedia/entry.html',{
        'title': markdown.markdown(util.get_entry(title))
    })
*/
editt = editing(initial={'textarea': 'entry'})
      return render(request, 'encyclopedia/edit.html',{
              'title': title,
              'editing': editt
          })
