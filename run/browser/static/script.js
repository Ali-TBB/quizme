/**
 * GET - get url parameters
 *
 * @param { string } name
 * @returns { string | undefined }
 */
function GET(name) {
  for (const item of location.search.substr(1).split("&")) {
    const tmp = item.split("=")

    if (tmp[0] === name) return decodeURIComponent(tmp[1])
  }

  return undefined
}

async function generateQuiz() {
  const quizTopic = $('#quiz-topic').val();
  const quizAttachment = $('#quiz-attachment').val();
  const quizDifficulty = $('#quiz-difficulty input:checked').val();
  const quizType = $('#quiz-type option:checked').val();
  const quizQuestionsNumber = $('#quiz-questions-number').val() * 1;

  let valid = true;

  if (!quizTopic || quizTopic === '') {
    $('#quiz-topic').addClass('is-invalid');
    $('#quiz-topic-feedback').text('Please enter a topic');
    valid = false;
  }

  if (quizAttachment) {
    const attachment = quizAttachment.split('.');
    const attachmentExtension = attachment[attachment.length - 1];
    const allowedExtensions = ['txt', 'pdf', 'doc', 'docx', 'png', 'jpg', 'jpeg'];
    console.log(attachmentExtension);

    if (allowedExtensions.indexOf(attachmentExtension) === -1) {
      $('#quiz-attachment').addClass('is-invalid');
      $('#quiz-attachment-feedback').text('The file extension is not allowed, allowed extensions are: ' + allowedExtensions.join(', '));
      valid = false;
    }
  }

  if (!quizQuestionsNumber) {
    $('#quiz-questions-number').addClass('is-invalid');
    $('#quiz-questions-number-feedback').text('Please enter a questions number');
    valid = false;
  } else if (quizQuestionsNumber < 1) {
    $('#quiz-questions-number').addClass('is-invalid');
    $('#quiz-questions-number-feedback').text('Please enter a valid questions number');
    valid = false;
  }

  if (!valid) return

  $('.form-control').removeClass('is-invalid');

  $('.container .loading').removeClass('hide');
  $('.container .content').addClass('hide');

  const formData = new FormData();
  formData.append('topic_content', quizTopic);
  formData.append('difficulty', quizDifficulty);
  formData.append('question_type', quizType);
  formData.append('number_of_questions', quizQuestionsNumber);
  if (quizAttachment) formData.append('attachment', $('#quiz-attachment')[0].files)

  try {
    const response = await $.post({
      url: '/generate_quiz',
      data: formData,
      cache: false,
      contentType: false,
      processData: false,
    });

    if (response && response.quiz_id && response.questions) {
      const { quiz_id: quizId, questions } = response;

      loadQuiz(quizId, quizTopic, quizDifficulty, quizType, quizQuestionsNumber, questions);
    }
  } catch (error) {
    console.error(error);
    
    alert('An error occurred, please try again later');
  }

  $('.container .loading').addClass('hide');
  $('.container .content').removeClass('hide');
}

function loadQuiz(quizId, quizTopic, quizDifficulty, quizType, quizQuestionsNumber, questions) {
  window.history.replaceState(undefined, 'Quiz Generator - #' + quizId, '?quiz_id=' + quizId);
  $('title').text('Quiz Generator - #' + quizId);

  $('#quiz-id-val').text(quizId);
  $('#quiz-topic-val').text(quizTopic);
  $('#quiz-difficulty-val').text(quizDifficulty);
  $('#quiz-type-val').text(quizType);
  $('#quiz-questions-number-val').text(quizQuestionsNumber);

  $('#quiz-body').empty();

  for (let i = 0; i < questions.length; i++) {
    const question = questions[i];
    $('#quiz-body').append(`
      <div class="question hide" id="question-${question.id}" data-index="${i}">
        <h3 class="bold">Question ${i+1}/${questions.length}: <span class="regular">${question.content}</span></h3>
        ${question.options.map((option, index) => {
          switch (question.question_type) {
            case 'one-answer':
              return `
                <div class="form-check">
                  <input class="form-check-input" type="radio" name="answer-${question.id}" id="answer-${question.id}-${option.id}" value="${option.id}">
                  <label class="form-check-label" for="answer-${question.id}-${option.id}">
                    ${option.option_text}
                  </label>
                </div>
              `;
            case 'multiple-answer':
              return `
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" name="answer-${question.id}-${option.id}" id="answer-${question.id}-${option.id}" value="${option.id}">
                  <label class="form-check-label" for="answer-${question.id}-${option.id}">
                    ${option.option_text}
                  </label>
                </div>
              `;
            default:
              break;
          }}).join('')}
      </div>
    `);
  }

  $('#quiz-body').attr('data-current-question', 0);
  $('#quiz-body').attr('data-questions-number', questions.length);
  $('.question[data-index="0"]').removeClass('hide');

  $('#get-started-header').addClass('hide');
  $('#quiz-header').removeClass('hide');

  $('#get-started-body').addClass('hide');
  $('#quiz-body').removeClass('hide');

  $('#get-started-footer').addClass('hide');
  $('#quiz-footer').removeClass('hide');
}

function nextQuestion() {
  const questions_number = parseInt($('#quiz-body').attr('data-questions-number'))
  let current_question = parseInt($('#quiz-body').attr('data-current-question'))

  if ($(`.question[data-index="${current_question}"] input:checked`).length === 0) {
    alert('Please select an answer');
    return;
  }

  if (current_question < questions_number - 1) {
    current_question++
    $('#quiz-body .question').addClass('hide')
    $(`.question[data-index="${current_question}"]`).removeClass('hide')
    $('#quiz-body').attr('data-current-question', current_question)
  }

  if (current_question === 0) {
    $('.btn[data-action="prev"]').addClass('hide')
  } else if (current_question > 0) {
    $('.btn[data-action="prev"]').removeClass('hide')
  }

  if (current_question === questions_number - 1) {
    $('.btn[data-action="next"]').addClass('hide')
    $('.btn[data-action="submit"]').removeClass('hide')
  }
}

function prevQuestion() {
  const questions_number = parseInt($('#quiz-body').attr('data-questions-number'))
  let current_question = parseInt($('#quiz-body').attr('data-current-question'))

  if (current_question > 0) {
    current_question--
    $('#quiz-body .question').addClass('hide')
    $(`.question[data-index="${current_question}"`).removeClass('hide')
    $('#quiz-body').attr('data-current-question', current_question)
  }

  if (current_question === 0) {
    $('.btn[data-action="prev"]').addClass('hide')
  } else if (current_question > 0) {
    $('.btn[data-action="prev"]').removeClass('hide')
  }

  if (current_question < questions_number - 1) {
    $('.btn[data-action="next"]').removeClass('hide')
    $('.btn[data-action="submit"]').addClass('hide')
  }
}

async function submitQuestion() {
  const questions_number = parseInt($('#quiz-body').attr('data-questions-number'))
  let current_question = parseInt($('#quiz-body').attr('data-current-question'))

  if ($(`.question[data-index="${current_question}"] input:checked`).length === 0) {
    alert('Please select an answer');
    return;
  }

  const answers = {};

  for (let i = 0; i < questions_number; i++) {
    const question = $(`.question[data-index="${i}"]`);
    const selectedAnswers = question.find('input:checked');

    answers[question.attr('id').split('-')[1]] = selectedAnswers.map((index, answer) => $(answer).val()).get();
  }

  $('.container .loading').removeClass('hide');
  $('.container .content').addClass('hide');

  try {
    const response = await $.post({
      url: `/quizzes/${$('#quiz-id-val').text()}`,
      data: {
        answers: JSON.stringify(answers),
      },
    });

    if (response && response.success) {
      for (let i = 0; i < response.results.results.length; i++) {
        $('#score-body').append(`<h4 class="bold">Question ${i+1}: <span class="regular">${response.results.results[i].is_correct ? 'Correct' : 'Incorrect'}</span></h4>`);
      }

      $('#score-body').append(`<h4 class="bold">Score: <span class="regular">${response.results.score}/100</span></h4>`);

      $('.container .header').addClass('hide');

      $('.container .body').addClass('hide');
      $('#score-body').removeClass('hide');

      $('.container .footer').addClass('hide');
      $('#score-footer').removeClass('hide');
    } else if (response && response.error) {
      alert(response.error);
    }
  } catch (error) {
    console.error(error);
    
    alert('An error occurred, please try again later');
  }

  $('.container .loading').addClass('hide');
  $('.container .content').removeClass('hide');
}

$('.btn[data-action="get_started"]').click(function () {
 generateQuiz()
});

$('.btn[data-action="next"]').click(function () {
  nextQuestion()
})

$('.btn[data-action="prev"]').click(function () {
  prevQuestion()
});

$('.btn[data-action="submit"]').click(function () {
  submitQuestion()
});

$('.btn[data-action="regenerate"]').click(function () {
  window.location.href = './single.html';
});

$(document).ready(async function () {
  const quizId = GET('quiz_id');

  if (quizId) {
    try {
      const response = await $.get({
        url: `/quizzes/${quizId}`,
      });

      if (response)
        if (response.success) {
          loadQuiz(response.quiz_id, response.topic_content, response.difficulty, response.question_type, response.number_of_questions, response.questions);
        } else if (response.error) {
          alert(response.error);
        }
    } catch (error) {
      console.error(error);
      
      alert('An error occurred, please try again later');
    }
  }
  
  $('.container .loading').addClass('hide');
  $('.container .content').removeClass('hide');
});
