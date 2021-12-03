from django.shortcuts import redirect, render
from .forms import ComputerForm
from .models import Computer


def computer_list(request):
    all_the_computers_in_my_function_based_view = Computer.objects.all()
    # print('I am in computer_list')
    # print(all_the_computers_in_my_function_based_view)
    context = {'all_the_computers': all_the_computers_in_my_function_based_view}
    return render(request, 'computer-list.html', context)


def computer_detail(request, **kwargs):
    # print(kwargs)
    computer_id = kwargs['pk']
    that_one_computer_in_my_function_based_view = Computer.objects.get(id=computer_id)
    # print(str(computer_id), " :: ", that_one_computer_in_my_function_based_view)
    context = {'that_one_computer': that_one_computer_in_my_function_based_view}
    return render(request, 'computer-detail.html', context)


def computer_create(request):
    if request.method == 'POST':
        # print("I am in POST")
        form_in_my_function_based_view = ComputerForm(request.POST)
        form_in_my_function_based_view.instance.myuser = request.user
        if form_in_my_function_based_view.is_valid():
            form_in_my_function_based_view.save()
            # print("I saved new computer")
        else:
            pass
            # print(form_in_my_function_based_view.errors)

        return redirect('computer-list')

    else:  # request.method == 'GET'
        # print("I am in GET")
        form_in_my_function_based_view = ComputerForm()
        context = {'form': form_in_my_function_based_view}
        return render(request, 'computer-create.html', context)
