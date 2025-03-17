from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Rattansi

class StudentRegistrationForm(UserCreationForm):
    student_number= forms.CharField(max_length=20, required=True, label='Registration number')
    
    class Meta:
        model=User
        fields=['username', 'student_number','email','password1','password2']
        
    def save(self, commit=True):
        user= super().save(commit=False)
        user.is_student= True
        user.student_number=self.cleaned_data['student_number']
        if commit:
            user.save()
            return user
class RattansiBursaryApplicationForm(forms.ModelForm):
    class Meta:
        model=Rattansi
        exclude=['student','application_status','amount_awarded','school_dean_comments','student_dean_comments']
        widgets={
            'gender':forms.Select(choices=[('M','Male'),('F','Female')]),
            'has_disability':forms.RadioSelect(choices=[(True,'Yes'),(False,'No')]),
            'sponsorship_status':forms.RadioSelect,
            'accomodation_status':forms.RadioSelect,
            'parental_Status':forms.RadioSelect,
            'on_work_study':forms.RadioSelect(choices=[(True,'Yes'),(False,'No')]),
            'external_support':forms.RadioSelect(choices=[(True,'Yes'),False,'No']),
            'ever_deferred':forms.RadioSelect(choices=[(True,'Yes'),(False,'No')]),
            'additional_info':forms.Textarea(attrs={'rows':4}),
        }
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args,**kwargs)
            # make disability details required if only has_disability is true
            self.fields['disability_details'].required= False
            
            # make parent details required based on parental status
            self.fields['father_age'].required=False
            self.fields['father_occupation'].required=False
            self.fields['father_employer'].required=False
            self.fields['father_health_status'].required=False
            self.fields['mother_age'].required=False
            self.fields['mother_occupation'].required=False
            self.fields['mother_employer'].required=False
            self.fields['mother_health_status'].required=False
            
            # make external support details required only if external_support is True
            self.fields['external_support_details'].required=False
            
            # make deferment reason reauired only if ever_deffered is True
            self.fields['deferred_reason'].required=False
            
            # add labels as shown in the form
            self.fields['school'].label="School"
            self.fields['gender'].label="Gender"
            self.fields['homeAdress'].label="Home Address"
            self.fields['telNo'].label="Telephone number"
            self.fields['homeCounty'].label="Home County"
            self.fields['subCounty'].label="Sub County"
            self.fields['next_of_kin_name'].label="Name of Next of Kin"
            self.fields['next_of_kin_address'].label="Adress "
            self.fields['next_of_kin_no'].label="Telephone number"
            self.fields['name_of_chief'].label="Name of Chief"
            self.fields['name_of_chief_adress'].label="Address"
            self.fields['name_of_chief_no'].label="Telephone number"
            self.fields['has_disability'].label="Are you living with any disability (Yes/No) "
            self.fields['disability_details'].label="if Yes,Specify "
            self.fields['sponsorship_status'].label="Student's status"
            self.fields['accomodation_status'].label="Accomodation or Residential Status"
            self.fields['parental_status'].label="Parental Status"
            self.fields['father_age'].label="Father's age"
            self.fields['fathers_occupation'].label="Father's occupation"
            self.fields['fathers_current_employee'].label="Father's current employer"
            self.fields['fathers_health_status'].label="Father's health status (Attach evidence)"
            self.fields['mother_age'].label="Mother's age"
            self.fields['mothers_occupation'].label="Mother's occupation"
            self.fields['mothers_current_employee'].label="Mother's current employer"
            self.fields['mothers_health_status'].label="Mother's health status (Attach evidence)"
            self.fields['total_sibling'].label="Total number of siblings (Excluding yourself)"
            self.fields['university_siblings'].label="No. of brothers/sisters in University/College/Tertiary institution"
            self.fields['secondary_siblings'].label="No of brothers/sisters in Secondary"
            self.fields['out_of_school_siblings'].label="How many siblings are out of school?"
            self.fields['out_of_school_reason'].label="Why are they out of school?"
            self.fields['working_siblings'].label="Any who are working and their occupations"
            self.fields['secondary_fee_payer'].label="Who paid your secondary school fee? (Attach evidence)"
            self.fields['on_work_study'].label="Are you/ have you been on work study program? (Attach evidence)"
            self.fields['external_support'].label="Did you receive any financial support from external sponnsors such as HELB, NGOs, CDF, "
            self.fields['external_support_details'].label="If yes, specify the financial support source and amount"
            self.fields['fee_balance'].label="Have you completed paying tuition fee if yes, specify the source and amount?"
            self.fields['ever_deferred'].label="Have you ever deferred your University studies"
            self.fields['deferment_reason'].label="If yes, give the reasons for your deferrement eg Medical/Social/Financial/Academic"
            self.fields['additional_info'].label="In the space, give any other relevant infomation that will help us make a decision about your level of need (Attach evidence)"
            self.fields['fee_statement'].label="Fee statement (PDF or Image)"
            self.fields['death_certificate'].label="Death certificate(if applicable)"
            self.fields['health_documents'].label="Health Documents(if applicable)"
            self.fields['other_documents'].label="Other supporting documents"
     



            

        
           


            
            
        