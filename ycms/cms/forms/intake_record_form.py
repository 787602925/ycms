import logging

from django.utils.translation import gettext_lazy as _

from ..constants import record_types
from ..models import MedicalRecord
from .custom_model_form import CustomModelForm

logger = logging.getLogger(__name__)


class IntakeRecordForm(CustomModelForm):
    """
    Form for creating intake records. Not used for general records.
    """

    class Meta:
        """
        This class contains additional meta configuration of the form class, see the :class:`django.forms.ModelForm`
        for more information.
        """

        model = MedicalRecord
        fields = ["patient", "diagnosis_code", "note"]

    def __init__(self, *args, **kwargs):
        r"""
        Initialize medical record form

        :param \*args: The supplied arguments
        :type \*args: list

        :param \**kwargs: The supplied keyword arguments
        :type \**kwargs: dict
        """
        initial_patient = kwargs.pop("initial_patient", None)
        super().__init__(*args, **kwargs)

        if initial_patient:
            initial = (
                initial_patient.id,
                f"{initial_patient.last_name}, {initial_patient.first_name}, {initial_patient.date_of_birth}",
            )
            self.fields["patient"].choices = [initial]
        else:
            self.fields["patient"].required = False
            self.fields["patient"].choices = [("", _("Search for existing patient"))]
        self.fields["diagnosis_code"].choices = [("", _("Search for diagnosis code"))]
        self.fields["diagnosis_code"].widget.attrs["class"] = "async_diagnosis_code"

    def save(self, commit=True):
        """
        This method extends the default ``save()``-method of the base :class:`~django.forms.ModelForm`
        to create a new intake record.

        :param commit: Whether or not the changes should be written to the database
        :type commit: bool

        :return: The saved medical record
        :rtype: ~ycms.cms.models.medical_record.MedicalRecord
        """
        cleaned_data = self.cleaned_data
        new_record = MedicalRecord.objects.create(
            creator=self.instance.creator,
            patient=self.instance.selected_patient,
            record_type=record_types.INTAKE,
            diagnosis_code=cleaned_data["diagnosis_code"],
            note=cleaned_data["note"],
        )
        return new_record
