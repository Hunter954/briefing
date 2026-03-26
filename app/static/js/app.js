document.addEventListener('DOMContentLoaded', () => {
  const steps = [...document.querySelectorAll('.step')];
  if (!steps.length) return;

  let currentStep = 0;
  const totalSteps = steps.length;
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const submitBtn = document.getElementById('submitBtn');
  const progressFill = document.getElementById('progressFill');
  const stepLabel = document.getElementById('stepLabel');
  const stepPercent = document.getElementById('stepPercent');
  const fileInput = document.getElementById('reference_images');
  const filePreview = document.getElementById('filePreview');
  const form = document.getElementById('briefingForm');

  const updateStep = () => {
    steps.forEach((step, index) => {
      step.classList.toggle('is-active', index === currentStep);
    });

    const percent = Math.round(((currentStep + 1) / totalSteps) * 100);
    progressFill.style.width = `${percent}%`;
    stepLabel.textContent = `Etapa ${currentStep + 1} de ${totalSteps}`;
    stepPercent.textContent = `${percent}%`;

    const isFirstStep = currentStep === 0;
    const isLastStep = currentStep === totalSteps - 1;

    prevBtn.style.visibility = isFirstStep ? 'hidden' : 'visible';
    nextBtn.classList.toggle('hidden', isLastStep);
    submitBtn.classList.toggle('hidden', !isLastStep);

    const stickyActions = document.querySelector('.sticky-actions');
    if (stickyActions) {
      stickyActions.classList.toggle('is-first-step', isFirstStep);
      stickyActions.classList.toggle('is-last-step', isLastStep);
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const validateCurrentStep = () => {
    const activeStep = steps[currentStep];
    const requiredFields = [...activeStep.querySelectorAll('[required]')];
    for (const field of requiredFields) {
      if (!field.value.trim()) {
        field.focus();
        field.reportValidity();
        return false;
      }
    }
    return true;
  };

  nextBtn?.addEventListener('click', () => {
    if (!validateCurrentStep()) return;
    if (currentStep < totalSteps - 1) {
      currentStep += 1;
      updateStep();
    }
  });

  prevBtn?.addEventListener('click', () => {
    if (currentStep > 0) {
      currentStep -= 1;
      updateStep();
    }
  });

  fileInput?.addEventListener('change', (event) => {
    const files = [...event.target.files];
    filePreview.innerHTML = '';
    files.forEach(file => {
      const chip = document.createElement('div');
      chip.className = 'file-chip';
      chip.textContent = file.name;
      filePreview.appendChild(chip);
    });
  });

  form?.addEventListener('submit', (event) => {
    const whatsapp = document.getElementById('contact_whatsapp');
    if (whatsapp) {
      whatsapp.value = (whatsapp.value || '').replace(/\D/g, '');
    }

    const requiredGlobal = ['brand_name', 'contact_name', 'contact_whatsapp'];
    for (const id of requiredGlobal) {
      const field = document.getElementById(id);
      if (field && !field.value.trim()) {
        event.preventDefault();
        currentStep = id === 'brand_name' ? 0 : totalSteps - 1;
        updateStep();
        field.focus();
        field.reportValidity();
        return;
      }
    }
  });

  updateStep();
});
